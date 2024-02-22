try:
    from flask import Flask, redirect, url_for, request, jsonify
    from flask_cors import CORS
    from routes.auth import auth_blueprint
    from utilities.db_connection import get_db_connection
    from utilities.session_manager import SessionManager
    from dotenv import load_dotenv
    import os
    import logging
    from logging.handlers import RotatingFileHandler
    from utilities.errors import ApiResponse
except ImportError as e:
    print("ERROR: One or more required modules are not installed! Please run 'pip install -r requirements.txt' to install them.")
    print(f"Exception data: {e}")
    exit(1)

logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler('log/app.log', maxBytes=10000, backupCount=3)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(handler)

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) 

app.config['SECRET_SESSION_KEY'] = os.environ.get('SECRET_SESSION_KEY')
app.config['DATABSE_URL'] = os.environ.get('DATABASE_URL')

app.db_connection = get_db_connection()
app.session_manager = SessionManager(app)

app.register_blueprint(auth_blueprint, url_prefix='/api/v1')

@app.route('/test')
def test_endpoint():
    return jsonify({"message": "your token was valid!"})

#? this middleware automatically checks the token for the user apart from specified endpoints
@app.before_request
def check_valid_login():
    # This list of endpoints doesn't require token authentication
    open_endpoints = ['auth.login', 'auth.register', 'static']

    if request.endpoint not in open_endpoints and not app.session_manager.is_session_valid():
        return ApiResponse.error("Session token was invalid", 401)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info("Firing up the backend")
    app.run(debug=True)