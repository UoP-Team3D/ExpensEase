import pytest
from io import BytesIO
from run import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_upload_receipt_success(client, mocker):
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)
    mocker.patch('utilities.session_manager.SessionManager.get_user_id', return_value=1)
    mocker.patch('models.receipt.Receipt.process_receipt', return_value=(100, 'Groceries'))

    mock_file = BytesIO(b'test file content')
    mock_file.name = 'test.jpg'

    response = client.post('/api/v1/receipt/upload', data={
        'receipt_image': (mock_file, 'test.jpg')
    }, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['data']['total_price'] == 100
    assert response.json['data']['category'] == 'Groceries'