from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta

def hash_password(password):
    return generate_password_hash(password).decode('utf8')

def check_password(password, hashed):
    return check_password_hash(hashed, password)

def create_token(identity):
    return create_access_token(identity=identity, expires_delta=timedelta(days=1))

def save_conversation(db, username, conversation):
    db.conversations.insert_one({"username": username, "conversation": conversation})
