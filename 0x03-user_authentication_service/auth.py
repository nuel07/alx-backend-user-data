#!/usr/bin/env python3
"""authentication module"""
import bcrypt


def _hash_password(password: str) -> str:
    """Returns salted hash of input password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
