import pytest
from run import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_get_expenses_success(client, mocker):
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)
    mocker.patch('utilities.session_manager.SessionManager.get_user_id', return_value=1)
    mocker.patch('models.expense.Expense.get_expenses', return_value=[{
        'expense_id': 1,
        'amount': 100,
        'description': 'Test expense',
        'date': '2023-01-01',
        'category': 'Test Category'
    }])

    response = client.get('/api/v1/expense/')

    assert response.status_code == 200
    assert response.json['success'] == True
    assert len(response.json['data']) == 1

def test_update_expense_success(client, mocker):
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)
    mocker.patch('utilities.session_manager.SessionManager.get_user_id', return_value=1)
    mocker.patch('models.expense.Expense.update_expense')

    response = client.put('/api/v1/expense/1', json={
        'amount': 150,
        'description': 'Updated expense'
    })

    assert response.status_code == 200
    assert response.json['success'] == True

def test_delete_expense_success(client, mocker):
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)
    mocker.patch('utilities.session_manager.SessionManager.get_user_id', return_value=1)
    mocker.patch('models.expense.Expense.delete_expense')

    response = client.delete('/api/v1/expense/1')

    assert response.status_code == 200
    assert response.json['success'] == True

def test_get_expenses_unauthorised(client):
    response = client.get('/api/v1/expense/')

    assert response.status_code == 401
    assert response.json['success'] == False

def test_update_expense_unauthorised(client):
    response = client.put('/api/v1/expense/1', json={
        'amount': 150,
        'description': 'Updated expense'
    })

    assert response.status_code == 401
    assert response.json['success'] == False

def test_delete_expense_unauthorised(client):
    response = client.delete('/api/v1/expense/1')

    assert response.status_code == 401
    assert response.json['success'] == False