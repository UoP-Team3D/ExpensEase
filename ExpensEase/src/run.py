from flask import Flask, jsonify
from flask_cors import CORS

# run.py 

app = Flask(__name__)
CORS(app)  # cors means cross-origin resource sharing, it allows us to make requests from the frontend to the backend even if they are on different domains or ports
           # it is a security feature that is enabled by default in most browsers, but we need to enable it in the backend as well

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello from Python backend!")

if __name__ == '__main__':
    app.run(debug=True, port=5000)