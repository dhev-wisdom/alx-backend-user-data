#!/usr/bin/env python3
"""
Authentification Module
"""

from api.v1.auth.auth import Auth
import base64
from flask import request
from models.user import User
from typing import List, TypeVar


class BasicAuth(Auth):
    """Basic Auth Class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if (
            path is None or
            path == "" or
            excluded_paths is None or
            len(excluded_paths) < 1
        ):
            return True
        if path[-1] != "/":
            path += "/"
        for path_ in excluded_paths:
            if path_ == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None:
            return None
        if request.headers.get("Authorization"):
            return request.headers.get("Authorization")
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """method to find the current user"""
        return None

    def extract_base64_authorization_header(self, authorization_header: str):
        """
        Base64 part of the Authorization header for a Basic Authentication
        """
        if (
                not authorization_header or
                not isinstance(authorization_header, str) or
                authorization_header[:6] != "Basic "
        ):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if (
                not base64_authorization_header or
                not isinstance(base64_authorization_header, str)
        ):
            return None
        try:
            original = base64.b64decode(base64_authorization_header)
            return original.decode("utf-8")
        except (TypeError, ValueError, UnicodeDecodeError):
            return None
        except binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value.
        """
        if (
                not decoded_base64_authorization_header or
                not isinstance(decoded_base64_authorization_header, str) or
                ":" not in decoded_base64_authorization_header
        ):
            return (None, None)

        name_email = decoded_base64_authorization_header.split(":")
        return (name_email[0], name_email[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        return the User instance based on his email and password
        """
        if (
                not user_email or not isinstance(user_email, str) or
                not user_pwd or not isinstance(user_pwd, str) or
                user_email == ""
        ):
            return None

        users = User.search({"email": user_email})
        if len(users) > 0:
            if users[0].is_valid_password(user_pwd):
                return users[0]
            return None
        return None