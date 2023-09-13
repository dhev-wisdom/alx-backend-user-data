#!/usr/bin/env python3
"""
Hashing passwordwith bcrypt
"""

from db import DB
import bcrypt
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password):
    """
    returns a hashed byte that represents password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        initialize Auth
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        pass
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = User(email=email, hashed_password=hashed_password)
            self._db.add_user(email, hashed_password)

        return user
