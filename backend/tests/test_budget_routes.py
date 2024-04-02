import pytest
from run import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_create_budget_success(client, mocker):
    # Mock the necessary functions and database interactions
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)
    mocker.patch('utilities.session_manager.SessionManager.get_user_id', return_value=1)
    mocker.patch('models.budget.Budget.create_budget', return_value=1)

    response = client.post('/api/v1/budget/create', json={
        'category_id': 1,
        'total_amount': 1000,
        'start_date': '2023-01-01',
        'end_date': '2023-12-31'
    })

    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['data']['budget_id'] == 1

def test_get_user_budgets_success(client, mocker):
    # Mock the necessary functions and database interactions
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)
    mocker.patch('utilities.session_manager.SessionManager.get_user_id', return_value=1)
    mocker.patch('models.budget.Budget.get_budgets_by_user', return_value=[{
        'budget_id': 1,
        'user_id': 1,
        'category_id': 1,
        'total_amount': 1000,
        'current_amount': 800,
        'start_date': '2023-01-01',
        'end_date': '2023-12-31'
    }])

    response = client.get('/api/v1/budget/')

    assert response.status_code == 200
    assert response.json['success'] == True
    assert len(response.json['data']) == 1