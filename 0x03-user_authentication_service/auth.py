#!/usr/bin/env python3
"""authentication module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """Returns salted hash of input password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return string representation of uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ return user object """
        if email and password:
            try:
                self._db.find_user_by(email=email)
            except NoResultFound:
                new_user = self._db.add_user(email, _hash_password(password))
                return new_user
            else:
                raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """validates user's password """
        try:
            new_user = self._db.find_user_by(email=email)
            if new_user:
                return bcrypt.checkpw(password.encode(),
                                      new_user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """returns sesion ID as a string"""
        try:
            new_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return "User doesn't exist"
        else:
            new_user.session_id = _generate_uuid()
            self._db.update_user(new_user.id, session_id=new_user.session_id)
            return new_user.session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """Find user by session ID"""
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """update user's session ID to None"""
        try:
            new_user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        new_user.session_id = None
