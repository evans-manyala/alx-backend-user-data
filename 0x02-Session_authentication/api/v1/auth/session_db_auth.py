#!/usr/bin/env python3

"""
This module implements session authentication that is saved in database.
"""
from datetime import datetime, timedelta
from typing import TypeVar, Union

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession as DBUserSession

UserSession = TypeVar("UserSession")


class SessionDBAuth(SessionExpAuth):
    """Implement Session Authentication with data persistence."""

    @staticmethod
    def get_db_session(session_id: str) -> Union[UserSession, None]:
        """Return the UserSession based on the `session_id`."""
        if not session_id:
            return None

        try:
            session: UserSession = DBUserSession.search(
                {"session_id": session_id})[0]
        except (KeyError, IndexError):
            return None

        return session

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """
        Create a user session and save the detail in a persistent
        storage.

        Args:
            user_id (str): The ID of the user to create the session for.

        Returns:
            str | None: The session ID is returned if everything goes
            alright, else None is returned if an invalid user ID was given.
        """
        session_id: Union[str, None] = super().create_session(user_id=user_id)
        if not session_id:
            return None

        session = DBUserSession(session_id=session_id,
                                user_id=user_id, id=session_id)
        session.save()

        return session.session_id

    def user_id_for_session_id(self, session_id:
                               str = None) -> Union[str, None]:
        """Return the User ID representing the UserSession in the database
        based on the `session_id`."""
        session = self.get_db_session(session_id=session_id)
        if not session:
            return None

        if self.session_duration <= 0:
            return session.user_id

        if not session.created_at:
            return None

        if datetime.now() > session.created_at + timedelta(
            seconds=self.session_duration
        ):
            return None

        return session.user_id

    def destroy_session(self, request=None) -> bool:
        """Delete user session from database."""
        if not request:
            return False

        session_id = self.session_cookie(request=request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id=session_id)
        if not user_id:
            return False

        session = self.get_db_session(session_id=session_id)
        if not session:
            return False

        session.remove()
        return True
