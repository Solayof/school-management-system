
from datetime import datetime, timedelta, timezone as tz
from os import getenv
from api.v1.auth.auth import Auth
from models.portal.session import Session
from models.portal.user import User


class SessionDbAuth(Auth):
    def __init__(self):
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "0"))
        except Exception:
            self.session_duration = 0
    
    def create_session(self, user_id=None):
        if user_id is None:
            return None
        user = User.get(user_id)
        if user is None:
            # user_id is not valid
            return None
        # Check if there is existing session by the user
        session = Session.query.filter(Session.user_id==user_id).one_or_none()
        # Check if the session is valid
        if session is not None:
            dur = timedelta(seconds=self.session_duration)
            if session.updated_at.replace(tzinfo=tz.utc) + dur > datetime.now(tz.utc):
                # Update the session if valid
                # Save the session update the session
                session.save()
                return session.id
            # Session not valid
            session.delete()
        # Create new session
        session = Session(user_id=user_id)
        session.save()
        return session.id

    def user_id_for_session_id(self, session_id=None):
        if session_id is None or isinstance(session_id, str) is False:
            return None
        # GEt the session
        session = Session.get(session_id)
        # if session exist
        if session is not None:
            dur = timedelta(seconds=self.session_duration)
            if session.updated_at.replace(tzinfo=tz.utc) + dur > datetime.now(tz.utc):
                # Session is valid
                return session.user_id
            # Session expired
            session.delete()
        return None
    
    def current_user(self, request=None):
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)
    
    def destory_sesion(self, request=None):
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None or self.user_id_for_session_id(cookie) is None:
            return False
        Session.get(cookie).delete()
        return True
