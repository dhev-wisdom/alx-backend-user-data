#!/usr/bin/env python3
"""
Password Hashing Module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Function hashes password using bcrypt
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if hashed_password correlates with password
    """
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    return False
