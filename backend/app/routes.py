from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import hash_password, check_password, create_token, save_conversation
from .ai_assistant import AI_Assistant

main = Blueprint('main', __name__)

@main.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    db = current_app.db
    if db.users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = hash_password(password)
    db.users.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "User created successfully"}), 201

@main.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    db = current_app.db
    user = db.users.find_one({"username": username})
    if not user or not check_password(password, user['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_token(identity=username)
    return jsonify({"token": token}), 200

@main.route('/start_interview', methods=['POST'])
@jwt_required()
def start_interview():
    current_user = get_jwt_identity()
    ai_assistant = AI_Assistant()
    greeting = "Thank you for applying to our company. I am here to interview you. Give me your introduction"
    
    ai_assistant.speak_text(greeting)
    ai_assistant.start_transcription()
    
    save_conversation(current_app.db, current_user, ai_assistant.full_transcript)
    return jsonify({"message": "Interview started"}), 200

@main.route('/test_db', methods=['GET'])
def test_db():
    db = current_app.db
    try:
        db.command('ping')
        return jsonify({"message": "Successfully connected to MongoDB"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

