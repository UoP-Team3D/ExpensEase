from flask import Blueprint, request, jsonify, current_app
from models.user import User  

auth_blueprint = Blueprint('api/auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    db_connection = current_app.db_connection

    data = request.json
    username = data.get('username')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    pin = data.get('pin')

    user = User(db_connection)
    try:
        user_id = user.register_user(username, email, first_name, last_name, password, pin)
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except Exception as e:
        db_connection.rollback()
        return jsonify({"error": str(e)}), 400