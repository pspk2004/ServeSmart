# This is the complete and final app.py file

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pymongo import MongoClient
from config import Config
import os
import certifi # <-- IMPORT THE NEW LIBRARY

db = None
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    global db
    try:
        mongo_uri = app.config['MONGO_URI']
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable not set.")
        
        # --- THE FINAL FIX IS HERE ---
        # We are telling MongoClient to use the certificate bundle from the 'certifi' library.
        # This solves SSL handshake issues on platforms like Vercel.
        ca = certifi.where()
        client = MongoClient(mongo_uri, tlsCAFile=ca)
        
        db = client.servesmart
        
        db.command('ping')
        print("MongoDB connection successful!")

    except Exception as e:
        # We will now print the initial connection error for better debugging
        print(f"CRITICAL: Initial MongoDB connection failed. Error: {e}")
        db = None

    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from routes import routes
        app.register_blueprint(routes)

    return app

app = create_app()