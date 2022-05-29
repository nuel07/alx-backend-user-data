#!/usr/bin/env python3
"""sessions database module"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """sessions database class representation"""

    def create_session(self, user_id=None):
        """create and store new instance of
        UserSession and return the session ID"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kwargs = {"user_id": user_id, "session_id": session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """return user ID based on Session ID from database"""
        if not session_id:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({
            "session_id": session_id})
        if not user_session:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """destroy user session based on session ID from cookie"""
        if not request:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        user_session = UserSession.search({
            "session_id": session_id})
        if not user_session:
            return None
        user_session = user_session[0]
        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return "An Error occurred!"
        return
