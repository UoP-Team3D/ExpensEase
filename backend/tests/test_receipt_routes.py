import os
import pytest
from run import create_app
from io import BytesIO

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_upload_receipt_success(client, mocker):
    mocker.patch('utilities.session_manager.SessionManager.is_session_valid', return_value=True)
    mocker.patch('utilities.session_manager.SessionManager.get_user_id', return_value=1)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_image_path = os.path.join(current_dir, 'test_images', 'holly.jpeg')

    with open(test_image_path, 'rb') as file:
        image_data = file.read()

    response = client.post('/api/v1/receipt/upload', data={
        'receipt_image': (BytesIO(image_data), 'holly.jpeg')
    }, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['data']['category'] == 'Eating Out'