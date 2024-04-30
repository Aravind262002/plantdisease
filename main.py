from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from disease_classifier import classify_disease
from disease_detector import predict_disease_boxes
from auth import Uploader


app = Flask(__name__)

# Create an instance of Uploader
db_instance = Uploader()

# Set the upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set the show folder
SHOW_FOLDER = "show"
if not os.path.exists(SHOW_FOLDER):
    os.makedirs(SHOW_FOLDER)

# Allowed extensions for image files
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


# Function to check if a file has an allowed extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if a file is provided
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        outfilePath = os.path.join(SHOW_FOLDER, filename)
        file.save(filepath)

        disease_name = classify_disease(filepath)
        predict_disease_boxes(filepath, outfilePath)

        # Construct the URL where the image is saved
        base_url = request.url_root.rstrip("/")
        image_url = f"{base_url}/show/{filename}"

        return jsonify({"image_url": image_url, "disease_name": disease_name}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400


@app.route("/show/<filename>", methods=["GET"])
def get_show_file(filename):
    return send_from_directory(SHOW_FOLDER, filename)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
