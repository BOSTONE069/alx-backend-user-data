#!/usr/bin/env python3
"""Database for the SQLALCHEMY"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from user import Base, User


class DB:
    """ DB class for the ORM"""

    def __init__(self):
        """Constructor Method"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Getter Session Method"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds user to database
        Return: User Object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """ Finds user by key word args
        Return: First row found in the users table as filtered by kwargs
        """
        if not kwargs:
            raise InvalidRequestError

        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise InvalidRequestError

        user = self.__session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user
