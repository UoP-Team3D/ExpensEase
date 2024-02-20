from flask import Flask, session, jsonify, request
from utilities.session_manager import SessionManager

app = Flask(__name__)
session_manager = SessionManager(app)

@app.route('/login', methods=['POST'])
def login():
    user_id = 'user123'
    token = session_manager.create_session(user_id)
    session['token'] = token 
    return f"Session created. Token: {token}"

@app.route('/verify', methods=['GET'])
def verify_session():
    session_token = session.get('token') 
    user_id = session_manager.get_user_id(session_token)
    if user_id:
        return f"Valid session for user ID: {user_id}"
    else:
        return "Invalid session", 401

@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.args.get('token')
    session_manager.end_session(session_id)
    return "Logged out"

if __name__ == '__main__':
    app.run(debug=True)
