from flask import Flask, session, current_app, make_response
from flask_session import Session
import os
from datetime import timedelta

class SessionManager:
    def __init__(self, app: Flask):
        # Set session secret key from environment variable
        app.config['SECRET_KEY'] = os.environ.get('SECRET_SESSION_KEY', 'default_secret_key')

        # Configure session to use filesystem
        app.config['SESSION_TYPE'] = 'filesystem'
        app.config['SESSION_PERMANENT'] = True
        app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
        app.config['SESSION_COOKIE_HTTPONLY'] = False  # Change this to True in production for security
        # Initialize the session
        Session(app)

    def create_session(self, user_id, app):
        session['user_id'] = user_id
        session.permanent = True  # Make the session permanent to use the expiry
        session.modified = True  # Mark the session as modified to update expiry time

        # Create a response object and set the session cookie
        response = make_response()
        
        # Set the session cookie with the appropriate attributes
        response.set_cookie(
            'session',
            session.sid,
            max_age=int(app.config['PERMANENT_SESSION_LIFETIME'].total_seconds()),
            secure=False,
            httponly=False,
            samesite='None',
            domain='127.0.0.1'
        )
        
        return response

    def get_user_id(self, session_id):
        return session.get('user_id')

    def refresh_session(self):
        session.modified = True  # Refresh the session expiry time

    def end_session(self, session_id):
        if session.sid == session_id:
            session.clear()

    def is_session_valid(self):
        user_id = session.get('user_id')
        return user_id is not None