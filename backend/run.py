from flask import Flask, jsonify, request, make_response, send_from_directory
from routes.auth import auth_blueprint
from routes.receipt import receipt_blueprint
from routes.budget import budget_blueprint
from routes.expense import expense_blueprint
from routes.category import category_blueprint
from utilities.db_connection import get_db_connection
from utilities.session_manager import SessionManager
from utilities.errors import ApiResponse
from dotenv import load_dotenv
from models.budget import socketio
import os
import logging
from logging.handlers import RotatingFileHandler

def create_app(test_config=None):
    app = Flask(__name__, static_folder='build')

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
    socketio.init_app(app)

    # Receipts dictionary to track receipts
    app.processed_receipts = {}

    cwd = os.getcwd()
    
    if os.path.basename(cwd) == "backend":
        log_dir = cwd
    else:
        log_dir = os.path.join(cwd, "backend")

    os.makedirs(os.path.join(log_dir, "log"), exist_ok=True)

    # Logging
    logging.basicConfig(level=logging.INFO)

    try:
        handler = RotatingFileHandler(os.path.join(log_dir, "log", "app.log"), maxBytes=10000, backupCount=3)
    except (FileNotFoundError, IOError):
        os.makedirs(os.path.join(log_dir, "log"), exist_ok=True)
        open(os.path.join(log_dir, "log", "app.log"), "w").close()
        handler = RotatingFileHandler(os.path.join(log_dir, "log", "app.log"), maxBytes=10000, backupCount=3)

    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(handler)

    # Blueprint registration
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    app.register_blueprint(receipt_blueprint, url_prefix='/api/v1/receipt')
    app.register_blueprint(budget_blueprint, url_prefix='/api/v1/budget')
    app.register_blueprint(expense_blueprint, url_prefix='/api/v1/expense')
    app.register_blueprint(category_blueprint, url_prefix='/api/v1/category')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    @app.before_request
    def check_valid_login():
        open_endpoints = ['auth.login', 'auth.register', 'static', 'root']
        if request.path.startswith('/api/v1/') and request.endpoint not in open_endpoints and not app.session_manager.is_session_valid():
            return ApiResponse.error("Session token was invalid!", 401)
    
    return app

if __name__ == '__main__':
    app = create_app()
    logger = logging.getLogger(__name__)
    socketio.run(app, debug=True)