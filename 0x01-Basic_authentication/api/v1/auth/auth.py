#!/usr/bin/env python3
"""Authentication class for the API"""

from flask import Flask, request
from typing import List, TypeVar


class Auth:
    """an authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns a boolean"""
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        if path is None or excluded_paths is None:
            return True
        path = path + '/' if path[-1] != '/' else path
        wildcard = any(req.endswith("*") for req in excluded_paths)
        if wildcard is None:
            if path in excluded_paths:
                return False
        for req in excluded_paths:
            if req[-1] == '*':
                if path.startswith(req[:-1]):
                    return False
            if req == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """return the value of the header request"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None
