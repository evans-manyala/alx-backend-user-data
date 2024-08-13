#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base


class DB:
    """
    DB class to manage Databse operations
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email address of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by filtering with the given keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments used to filter
            the users table.

        Returns:
            User: The first User object that matches the filter criteria.

        Raises:
            NoResultFound: If no results are found matching the criteria.
            InvalidRequestError: If the query arguments are invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user found matching the criteria.")
            return user
        except Exception as e:
            raise InvalidRequestError("Invalid query arguments.") from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes based on the provided keyword arguments.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments used to update the
            user's attributes.

        Raises:
            InvalidRequestError: If the update arguments are invalid.
        """

        user = self.find_user_by(id=user_id)
        valid_attributes = {"email", "hashed_password", "session_id",
                            "reset_token"}
        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        self._session.commit()