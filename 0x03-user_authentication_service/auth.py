#!/usr/bin/env python3
"""
Hashing passwordwith bcrypt
"""

from db import DB
import bcrypt
from user import User
import uuid
from sqlalchemy.exc import NoResultFound


def _hash_password(password):
    """
    returns a hashed byte that represents password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    generate a new uuid
    """
    return str(uuid.uuid4())


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
        register user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = User(email=email, hashed_password=hashed_password)
            self._db.add_user(email, hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate login
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        create session
        """
        try:
            user = self._db.find_user_by(email=email)
            uuid_ = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=uuid_)
            return uuid_
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Find user by session id
        """
        user = self._db.find_user_by(session_id=session_id)
        if user is not None:
            return user
        return None

    def destroy_session(self, user_id: int) -> None:
        """
        removes session_id from user with id user_id
        """
        user = self._db.find_user_by(id=user_id)
        if user:
            self._db.update_user(user_id=user.id, session_id=None)
            return None
        print("Invalid user id. User not found")
