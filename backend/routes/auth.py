from flask import Blueprint, request, current_app, make_response, jsonify, session
from models.user import User  
from utilities.errors import ApiResponse
from utilities.session_manager import SessionManager
import re
from flask_cors import CORS, cross_origin

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
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
            session_id = session.sid
            response = session_manager.create_session(user_id, current_app)
            current_app.session_manager.create_session(user_id, current_app)  # Assuming session creation
            
            info = {"success": True, "message": "Login successful", "sessionToken": session_id}
            resp = make_response(jsonify(info), 200)
            # Set cookie normally as you have in your original code
            resp.set_cookie('session', session_id, max_age=30*24*60*60, secure=False, httponly=True, samesite='Lax')            
            return resp
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


@auth_blueprint.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    current_password = data.get('password')
    new_password = data.get('new_password')
    db_connection = current_app.db_connection
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not session.sid:
        return ApiResponse.error("No session token at all!", status=401)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    user = User(db_connection)

    # Validate input
    if not all([current_password, new_password]):
        current_app.logger.warning("Make sure to enter current password and new password.")
        return ApiResponse.error("Current password and new password are required.", status=400)

    if len(new_password) < 8 or not re.search(r'\d', new_password): #? where \d is a value, if password isnt >8 characters long and doesn't have a number
        return ApiResponse.error("Password must be at least 8 characters and contain a number.", status=400)

    if new_password == current_password:
        return ApiResponse.error("The new password can not be the same as the current password!", status=400)

    try:
        if user.change_password(user_id, current_password, new_password):
            return ApiResponse.success(message="Password updated successfully.")
        else:
            return ApiResponse.error("Invalid password.", status=500)
    
    except Exception as e:
        current_app.logger.error(f"Error during password update: {e}")
        return ApiResponse.error("An internal error occurred during password update.", status=500)

@auth_blueprint.route('/delete_account', methods=['DELETE'])
def delete_account():
    db_connection = current_app.db_connection
    session_manager = current_app.session_manager
    user = User(db_connection)

    if not session.sid:
        return ApiResponse.error("No session token at all!", status=401)

    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    try:
        if user.delete_user(user_id):
            session_manager.end_session(session.sid)
            response = make_response(ApiResponse.success(message="Account deleted successfully"))
            response.delete_cookie('session')
            return response
        else:
            return ApiResponse.error("An internal error occurred during account deletion.", status=500)

    except Exception as e:
        current_app.logger.error(f"Error during account deletion: {e}")
        return ApiResponse.error("An internal error occurred during account deletion.", status=500)
    
@auth_blueprint.route('/change_email', methods=['POST'])  
def change_email():
    data = request.json
    current_email = data.get('current_email')
    new_email = data.get('new_email')
    db_connection = current_app.db_connection
    session_manager = current_app.session_manager
    user = User(db_connection)
    user_id = session_manager.get_user_id(session.sid)

    if not session.sid:
        return ApiResponse.error("No session token at all!", status=401)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    if not new_email or not current_email:
        current_app.logger.warning("Make sure the new email and current_email exists!")
        return ApiResponse.error("Both emails is required.", status=400)
   
    try:
        if user.update_email(current_email, new_email, user_id):
            return ApiResponse.success(message="Email updated successfully.")

        else:
            return ApiResponse.error("Email wasn't the same or there was an error!", status=500)
            
    except Exception as e:
        current_app.logger.error(f"Error during email update: {e}")
        return ApiResponse.error("An internal error occurred during email update.", status=500)
