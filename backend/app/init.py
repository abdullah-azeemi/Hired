from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    print("Creating Flask app")
    app = Flask(__name__)
    app.config.from_object(Config)

    print("Initializing Bcrypt and JWTManager")
    bcrypt.init_app(app)
    jwt.init_app(app)

    print("Connecting to MongoDB")
    uri = app.config['MONGO_URI']
    db_name = 'test'
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    app.db = client[db_name]  # Explicitly use the database name

    from .routes import main
    app.register_blueprint(main)

    return app
