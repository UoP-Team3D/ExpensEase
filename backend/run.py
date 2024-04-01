from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.auth import auth_blueprint
from routes.receipt import receipt_blueprint
from routes.budget import budget_blueprint
from routes.expense import expense_blueprint
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

    # Receipts dictionary to track receipts
    app.processed_receipts = {}

    # Logging
    logging.basicConfig(level=logging.INFO)
    handler = RotatingFileHandler('log/app.log', maxBytes=10000, backupCount=3)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(handler)

    # Blueprint registration
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    app.register_blueprint(receipt_blueprint, url_prefix='/api/v1/receipt')
    app.register_blueprint(budget_blueprint, url_prefix='/api/v1/budget')
    app.register_blueprint(expense_blueprint, url_prefix='/api/v1/expense')

    # Setup cross-origin resource sharing
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Basic API welcome message on root
    @app.route('/')
    def root():
        return jsonify({"message": "Welcome to the ExpensEase API!"})

    # Middleware for session validation on closed endpoints, security
    @app.before_request
    def check_valid_login():
        open_endpoints = ['auth.login', 'auth.register', 'static', 'root']
        if request.endpoint not in open_endpoints and not app.session_manager.is_session_valid():
            return ApiResponse.error("Session token was invalid", 401)

    return app

if __name__ == '__main__':
    app = create_app()
    logger = logging.getLogger(__name__)

   # scheduler = BackgroundScheduler()
   # scheduler.add_job(check_budget_notifications, 'interval', minutes=1, args=[app])
   # scheduler.start()

    app.run(debug=True)