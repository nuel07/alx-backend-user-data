#!/usr/bin/env python3
""" Session authentication mechanism """

from api.v1.auth.auth import Auth
from models.user import User
import base64
from flask import request
import uuid
from typing import List, TypeVar


class SessionAuth(Auth):
    """ Session authentication class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ instance method that creates a session ID for a user_id """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a user ID based on the session ID """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        session_cookie = self.session_cookie(request)
        session_id = self.user_id_for_session_id(session_cookie)
        the_user = User.get(session_id)
        return the_user

    def destroy_session(self, request=None):
        """ deletes the user session / logout"""
        if not request:
            return False

        session_id_cookie = self.session_cookie(request)
        if not session_id_cookie:
            return False

        user_id = self.user_id_for_session_id(session_id_cookie)
        if not user_id:
            return False

        self.user_id_by_session_id.pop(session_id_cookie)
        return True
