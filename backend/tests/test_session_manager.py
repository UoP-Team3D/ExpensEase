import pytest
from flask import Flask, session
from datetime import timedelta
from unittest.mock import patch, MagicMock
from utilities.session_manager import SessionManager

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
    app.config['SESSION_COOKIE_HTTPONLY'] = False
    return app

@pytest.fixture
def session_manager(app):
    return SessionManager(app)

def test_create_session(app, session_manager):
    user_id = 1
    with app.test_request_context():
        response = session_manager.create_session(user_id, app)
        assert response.status_code == 200
        assert response.headers['Set-Cookie'].startswith('session=')
        assert 'Max-Age=2592000' in response.headers['Set-Cookie']
        assert 'SameSite=None' in response.headers['Set-Cookie']
        assert 'Domain=127.0.0.1' in response.headers['Set-Cookie']

def test_get_user_id(app, session_manager):
    user_id = 1
    with app.test_request_context():
        session_manager.create_session(user_id, app)
        retrieved_user_id = session_manager.get_user_id(None)
        assert retrieved_user_id == user_id

def test_refresh_session(app, session_manager):
    with app.test_request_context():
        session['user_id'] = 1
        session_manager.refresh_session()
        assert session.modified

def test_end_session(app, session_manager):
    with app.test_request_context():
        session['user_id'] = 1
        session_manager.end_session(session.sid)
        assert 'user_id' not in session

def test_is_session_valid(app, session_manager):
    with app.test_request_context():
        session['user_id'] = 1
        assert session_manager.is_session_valid()

    with app.test_request_context():
        session.clear()
        assert not session_manager.is_session_valid()