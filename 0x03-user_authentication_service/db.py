#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base
User = __import__('user').User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized sessiion object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    
    def add_user(self, email: str, hashed_password: str) -> User:
        """Returns user object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user


    def find_user_by(self, **kwargs) -> User:
        """Return first row found in users table
        """
        try:
            new_user = self._session.query(User).filter_by(**kwargs).first()
        except TypeError:
            raise InvalidRequestError
        if not new_user:
            raise NoResultFound
        return new_user


    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user
        """
        new_usr = self.find_user_by(id=user_id)
        attrbtes = {k:v for k, v in kwargs.items() if v}
        for key in kwargs.keys():
            if key not in User.__table__.columns.keys():
                raise ValueError
        self._session.commit()
