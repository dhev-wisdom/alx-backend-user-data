#!/usr/bin/env python3
"""
Hashing passwordwith bcrypt
"""

import bcrypt


def _hash_password(password):
    """
    returns a hashed byte that represents password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


if __name__ == "__main__":
    _hash_password(password)
