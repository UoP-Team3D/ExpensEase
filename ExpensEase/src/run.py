from flask import Flask
from routes.auth import auth_blueprint
from utilities.db_connection import get_db_connection
from utilities.session_manager import SessionManager

app = Flask(__name__)

app.db_connection = get_db_connection()
app.session_manager = SessionManager(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
