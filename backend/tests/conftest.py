import pytest
import os
from run import create_app
from utilities.db_connection import get_db_connection

from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def app():
    os.environ['DATABASE_URL'] = os.getenv('TEST_DATABASE_URL')
    app = create_app({'TESTING': True})
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return get_db_connection()
