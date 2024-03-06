import pytest
from flask import Flask, jsonify
from utilities.errors import ApiResponse

@pytest.fixture
def app_context():
    app = Flask(__name__)
    app.config['TESTING'] = True
    with app.app_context():
        yield app

def test_api_response_success(app_context):
    response, status = ApiResponse.success(message="Test Success")
    assert status == 200
    assert response.json == {"success": True, "message": "Test Success"}

    response, status = ApiResponse.success(message="Test Success", data={"key": "value"})
    assert status == 200
    assert response.json == {"success": True, "message": "Test Success", "data": {"key": "value"}}

def test_api_response_error(app_context):
    response, status = ApiResponse.error(message="Test Error")
    assert status == 400
    assert response.json == {"success": False, "message": "Test Error"}

    response, status = ApiResponse.error(message="Test Error", status=500)
    assert status == 500
    assert response.json == {"success": False, "message": "Test Error"}
