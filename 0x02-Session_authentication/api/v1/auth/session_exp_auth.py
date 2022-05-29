#!/usr/bin/env python3
"""session expiration module"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session expiration class"""
    def __init__(self):
        """initialization of instance"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create user session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """return user for session dictionary"""
        if not session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        the_user = session_dict.get('user_id')
        if the_user:
            if self.session_duration <= 0:
                return the_user
            created_at = session_dict.get('created_at')
            if not created_at:
                return None
            if (created_at + timedelta
                (seconds=self.session_duration) < datetime.now()):
                return None
            return the_user
