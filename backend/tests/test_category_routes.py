import pytest
from run import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_create_category_success(client, mocker):
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)
    mocker.patch('utilities.session_manager.SessionManager.get_user_id', return_value=1)
    mocker.patch('models.category.Category.create_category', return_value=1)

    response = client.post('/api/v1/category/', json={
        'category_name': 'New Category'
    })

    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['data']['category_id'] == 1

def test_get_user_categories_success(client, mocker):
    # Mock the necessary functions and database interactions
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)
    mocker.patch('utilities.session_manager.SessionManager.get_user_id', return_value=1)
    mocker.patch('models.category.Category.get_categories_by_user', return_value=[{
        'category_id': 1,
        'user_id': 1,
        'category_name': 'Test Category',
        'is_preset': False
    }])

    response = client.get('/api/v1/category/')

    assert response.status_code == 200
    assert response.json['success'] == True
    assert len(response.json['data']) == 1

