from auth import Uploader
from flask import Flask, request, jsonify

app = Flask(__name__)

# Create an instance of Uploader
db_instance = Uploader()

@app.route('/register', methods=['POST'])
def register():
    # Get JSON data from the request body
    data = request.get_json()

    # Extract username, email, and password from JSON data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if all required fields are present
    if not (username and email and password):
        return jsonify({'message': 'Missing required fields', "ok": False}), 400
    
    # upload data
    db_instance.upload(username, email, password)

    return jsonify({'message': 'Data Uploaded Successfully!', "ok": True})

@app.route('/login', methods=['POST'])
def login():
    # Get JSON data from the request body
    data = request.get_json()

    # Extract username and password from JSON data
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are provided
    if not (username and password):
        return jsonify({'message': 'Missing username or password', "ok": False}), 400

    # Get data from the uploader
    user_data = db_instance.get_data()

    # Check if the provided username exists in the user data
    if username not in user_data:
        return jsonify({'message': 'Username not found', "ok": False}), 401

    # Check if the provided password matches the password associated with the username
    if user_data[username]['password'] != str(password):
        return jsonify({'message': 'Incorrect password', "ok": False}), 401

    # If username and password match, return success message
    return jsonify({'message': 'Login Successful!', "ok": True})

@app.route('/')
def index():
    return "Server Started!"
    
if __name__ == '__main__':
    app.run(debug=True)