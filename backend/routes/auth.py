from flask import Blueprint, request, current_app, make_response, session
from models.user import User  
from utilities.errors import ApiResponse
from utilities.session_manager import SessionManager
import re

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1')

@auth_blueprint.route('/register', methods=['POST'])
def register():
    """
    Endpoint for user registration. It receives user data, validates it, 
    and attempts to register a new user. Returns a success response with user ID 
    on successful registration or an error response otherwise.

    Args:
        None

    Returns:
        Flask Response object: JSON response with registration status.
    """
    db_connection = current_app.db_connection

    data = request.json
    username = data.get('username')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    pin = data.get('pin')

    # Validate input
    if not all([username, email, first_name, last_name, password, pin]):
        current_app.logger.warning("Every field, username, email, first_name, last_name, password, pin has to exist in the json")
        return ApiResponse.error("All fields are required.", status=400)

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return ApiResponse.error("Invalid email format.", status=400)

    if len(pin) != 4 or not pin.isdigit():
        return ApiResponse.error("PIN must be a 4 digit number.", status=400)

    # Password validation: at least 8 characters and contains one number (regex is slow but oh well)
    if len(password) < 8 or not re.search(r'\d', password): #? where \d is a value, if password isnt >8 characters long and doesn't have a number
        return ApiResponse.error("Password must be at least 8 characters and contain a number.", status=400)

    user = User(db_connection)
    try:
        user_id = user.register_user(username, email, first_name, last_name, password, pin)
        return ApiResponse.success(message="User registered successfully", data={"user_id": user_id})
    except ValueError as e: #? email or password already exists in the database
        return ApiResponse.error(str(e), status=400)
    except Exception as e:
        db_connection.rollback()
        current_app.logger.error(f"Error registering user: {e}")
        return ApiResponse.error("An internal error occurred during registration.", status=500)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login. It receives username and password, 
    authenticates them, and returns a success response if the 
    authentication is successful, or an error response otherwise.

    Args:
        None

    Returns:
        Flask Response object: JSON response with login status.
    """
    db_connection = current_app.db_connection
    session_manager = current_app.session_manager

    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Validate input
    if not all([username, password]):
        current_app.logger.warning(f"Make sure the username and password are in the JSON!")
        return ApiResponse.error("Username and password are required.", status=400)

    user = User(db_connection)
    try:
        success, user_id = user.login(username, password)
        if success:
            session_manager.create_session(user_id)
            return ApiResponse.success(message="Login successful")
        else:
            return ApiResponse.error("Invalid username or password.", status=401) 
        
    except Exception as e:
        current_app.logger.error(f"Error during login: {e}")
        return ApiResponse.error("An internal error occurred during login.", status=500)


@auth_blueprint.route('/logout', methods=['DELETE'])
def logout():
    """
    Endpoint for user logout. It ends the user's session and clears the session cookie.

    Args:
        None

    Returns:
        Flask Response object: JSON response indicating logout success.
    """
    session_manager = current_app.session_manager

    try:
        session_manager.end_session(session.sid)
        response = make_response(ApiResponse.success(message="Logout successful"))

        response.delete_cookie('session')
        return response
    except Exception as e:
        current_app.logger.error(f"Error during logout: {e}")
        return ApiResponse.error("An internal error occurred during logout.", status=500)

@auth_blueprint.route('/reset_password', methods=['GET'])
def reset_password():
    data = request.json
    email = data.get('email')
    if not email:
        return ApiResponse.error("Email is required.", status=400)
    user = User(current_app.db_connection)
    user_data = user.get_user_by_email(email)

    if user_data:
        token = f"mock_token_for_{email}"
        current_app.logger.info(f"Send this token to the user's email: {token}")
        return ApiResponse.success(message="Password reset token sent.")
    else:
        return ApiResponse.error("No user found with that email.", status=404)
    
@auth_blueprint.route('/reset_password/<token>', methods=['GET'])
def reset_password_token(token):
        data = request.json
        new_password = data.get('new_password')
        if not new_password:
            return ApiResponse.error("New password is required.", status=400)
        
        if not token.startswith("mock_token_for_"):
            return ApiResponse.error("Invalid token.", status=400)
        
        email = token.replace("mock_token_for_", "")
        user = User(current_app.db_connection)
        if user.update_password(email, new_password):
            return ApiResponse.success(message="Password updated successfully.")
        else:
            return ApiResponse.error("An internal error occurred during password reset.", status=500)