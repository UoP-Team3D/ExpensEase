import pytest
from run import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_register_success(client, mocker):
    # Mocking database interaction
    mocker.patch('models.user.User.register_user', return_value=1)
    
    # Simulate a post request to the register endpoint
    response = client.post('/api/v1/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User',
        'password': 'password123',
        'pin': '1234'
    })

    assert response.status_code == 200
    assert response.json['success'] == True

def test_register_failure(client, mocker):
    # Mocking database interaction
    mocker.patch('models.user.User.register_user', side_effect=ValueError("User already exists"))

    response = client.post('/api/v1/register', json={
        'username': 'existinguser',
        'email': 'existinguser@example.com',
        'first_name': 'Existing',
        'last_name': 'User',
        'password': 'password123',
        'pin': '1234'
    })

    assert response.status_code == 400
    assert "User already exists" in response.json['message']

def test_register_failure_email(client, mocker):
    # Mocking database interaction
    mocker.patch('models.user.User.register_user', side_effect=ValueError("User already exists"))

    response = client.post('/api/v1/register', json={
        'username': 'brandnewuser',
        'email': 'fakeemail',
        'first_name': 'Existing',
        'last_name': 'User',
        'password': 'password123',
        'pin': '1234'
    })

    assert response.status_code == 400
    assert "Invalid email format." in response.json['message']

def test_register_failure_not_filled(client, mocker):
    # Mocking database interaction
    mocker.patch('models.user.User.register_user', side_effect=ValueError("User already exists"))

    response = client.post('/api/v1/register', json={
        'username': 'brandnewuser',
        'email': 'fakeemail',
        'first_name': '',
        'last_name': '',
        'password': 'password123',
        'pin': '1234'
    })

    assert response.status_code == 400
    assert "All fields are required." in response.json['message']

def test_weak_password(client, mocker):
    # Mocking database interaction
    mocker.patch('models.user.User.register_user', side_effect=ValueError("User already exists"))

    response = client.post('/api/v1/register', json={
        'username': 'brandnewuser',
        'email': 'existinguser@example.com',
        'first_name': 'Existing',
        'last_name': 'User',
        'password': 'weak',
        'pin': '1234'
    })

    assert response.status_code == 400
    assert "Password must be at least 8 characters and contain a number." in response.json['message']

def test_register_failure_pin(client, mocker):
    # Mocking database interaction
    mocker.patch('models.user.User.register_user', side_effect=ValueError("User already exists"))

    response = client.post('/api/v1/register', json={
        'username': 'brandnewuser',
        'email': 'brandnewuser@example.com',
        'first_name': 'Existing',
        'last_name': 'User',
        'password': 'password123',
        'pin': 'badpin'
    })

    assert response.status_code == 400
    assert "PIN must be a 4 digit number." in response.json['message']

def test_login_success(client, mocker):
    # Mock User login method
    mocker.patch('models.user.User.login', return_value=(True, 1))

    # Mock SessionManager's create_session method
    mocker.patch('utilities.session_manager.SessionManager.create_session')

    response = client.post('/api/v1/login', json={
        'username': 'existinguser',
        'password': 'correctpassword'
    })

    assert response.status_code == 200
    assert response.json['success'] == True

def test_logout_success(client, mocker):
    # Mock SessionManager's is_session_valid method to return True, simulating a logged-in state
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)

    # Mock SessionManager's end_session method
    mocker.patch('utilities.session_manager.SessionManager.end_session')

    response = client.delete('/api/v1/logout')

    assert response.status_code == 200
    assert response.json['success'] == True

def test_middleware(client, mocker):
    # Should 401 if the before request middleware is set up properly
    response = client.delete('/api/v1/logout')
    assert response.status_code == 401 