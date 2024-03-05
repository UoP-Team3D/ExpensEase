import pytest
from models.user import User
import bcrypt

# Constants for testing
USERNAME = "testuser"
EMAIL = "test@example.com"
FIRST_NAME = "Test"
LAST_NAME = "User"
PASSWORD = "password123"
PIN = "1234"

@pytest.fixture
def setup_test_user(db):
    # Pre-test cleanup: ensure the test user does not already exist
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM public.\"Users\" WHERE username = %s OR email = %s", (USERNAME, EMAIL))
        db.commit()

    user = User(db)
    user_id = user.register_user(USERNAME, EMAIL, FIRST_NAME, LAST_NAME, PASSWORD, PIN)
    yield user_id  # This value is returned to the test

    # Post-test cleanup
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM public.\"Users\" WHERE username = %s", (USERNAME,))
        db.commit()

def test_user_creation_and_duplication(db, setup_test_user):
    user = User(db)

    # Fetch the newly created user from the database
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM public.\"Users\" WHERE username = %s", (USERNAME,))
        created_user = cursor.fetchone()
    
    assert created_user is not None
    assert created_user[1] == USERNAME 
    assert created_user[2] == EMAIL  

    # Test duplicate username and email
    with pytest.raises(ValueError):
        user.register_user(USERNAME, "newemail@example.com", FIRST_NAME, LAST_NAME, PASSWORD, PIN)

    with pytest.raises(ValueError):
        user.register_user("newusername", EMAIL, FIRST_NAME, LAST_NAME, PASSWORD, PIN)

def test_password_hashing(db, setup_test_user):
    user = User(db)
    with db.cursor() as cursor:
        cursor.execute("SELECT password FROM public.\"Users\" WHERE username = %s", (USERNAME,))
        stored_password = cursor.fetchone()[0]

    assert stored_password is not None
    assert stored_password != PASSWORD
    assert bcrypt.checkpw(PASSWORD.encode('utf-8'), stored_password.encode('utf-8'))

def test_successful_login(db, setup_test_user):
    user = User(db)
    success, user_id = user.login(USERNAME, PASSWORD)
    assert success is True
    assert user_id is not None

def test_incorrect_password_login(db, setup_test_user):
    user = User(db)
    wrong_password = "wrongpassword"
    success, user_id = user.login(USERNAME, wrong_password)
    assert success is False
    assert user_id is None

def test_nonexistent_user_login(db):
    user = User(db)
    non_existent_username = "nonexistentuser"
    success, user_id = user.login(non_existent_username, PASSWORD)
    assert success is False
    assert user_id is None

def test_user_data_integrity(db, setup_test_user):
    user = User(db)
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM public.\"Users\" WHERE username = %s", (USERNAME,))
        created_user = cursor.fetchone()

    assert created_user is not None
    assert created_user[1] == USERNAME
    assert created_user[2] == EMAIL
    assert created_user[3] == FIRST_NAME
    assert created_user[4] == LAST_NAME