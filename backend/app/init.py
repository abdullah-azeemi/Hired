from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from .routes import main

def create_app():
    app = Flask(__name__, static_folder='./static')
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    # Connect to MongoDB
    uri = "mongodb+srv://abdullahmusharaf200:60JMTqE3R2xhRQOz@aitutor.3v9fdyy.mongodb.net/?retryWrites=true&w=majority&appName=AITutor"
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    app.db = client.get_database("test")  

    app.register_blueprint(main)

    return app
