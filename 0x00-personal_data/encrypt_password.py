#!/usr/bin/env python3
"""
Password Hashing Module
"""

import bcrypt


def hash_password(password: str):
    """
    Function hashes password using bcrypt
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed
