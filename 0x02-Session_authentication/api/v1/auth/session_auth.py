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
