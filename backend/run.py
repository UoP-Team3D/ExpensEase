from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.auth import auth_blueprint
from utilities.db_connection import get_db_connection
from utilities.session_manager import SessionManager
from utilities.errors import ApiResponse
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

def create_app(test_config=None):
    app = Flask(__name__)

    # Load default or test configuration
    if test_config is not None:
        app.config.update(test_config)
    else:
        load_dotenv()
        app.config['SECRET_SESSION_KEY'] = os.environ.get('SECRET_SESSION_KEY')
        app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')

    # Database and session manager setup
    app.db_connection = get_db_connection()
    app.session_manager = SessionManager(app)

    # Logging
    logging.basicConfig(level=logging.INFO)
    handler = RotatingFileHandler('log/app.log', maxBytes=10000, backupCount=3)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(handler)

    # Blueprint registration
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/test')
    def test_endpoint():
        return jsonify({"message": "your token was valid!"})

    @app.before_request
    def check_valid_login():
        open_endpoints = ['auth.login', 'auth.register', 'static']
        if request.endpoint not in open_endpoints and not app.session_manager.is_session_valid():
            return ApiResponse.error("Session token was invalid", 401)

    return app

if __name__ == '__main__':
    app = create_app()
    logger = logging.getLogger(__name__)
    logger.info("Firing up the backend")
    app.run(debug=True)
