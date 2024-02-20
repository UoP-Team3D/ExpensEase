from flask import Flask, session
from flask_session import Session
import os

class SessionManager:
    def __init__(self, app: Flask):
        app.config['SESSION_TYPE'] = 'filesystem' # use files for now
        app.config['SESSION_PERMANENT'] = False
        app.secret_key = os.urandom(24)

        Session(app)

    def create_session(self, user_id):
        session['user_id'] = user_id
        return session.sid

    def get_user_id(self, session_id):
        if session.sid == session_id:
            return session.get('user_id')
        return None

    def end_session(self, session_id):
        if session.sid == session_id:
            session.clear()

    # TODO: add token refreshing, token expiry, blah blah