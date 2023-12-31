#!/usr/bin/env python3
"""
Authentification Module
"""

from flask import request
import fnmatch
from typing import List, TypeVar


class Auth():
    """Auth Class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if (
            path is None or
            path == "" or
            excluded_paths is None or
            len(excluded_paths) < 1
        ):
            return True

        for path_ in excluded_paths:
            if fnmatch.fnmatch(path, path_):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """method to find the current user"""
        return None
