# --- This is the complete and corrected app.py file ---
print("--- RUNNING THE NEW, CORRECTED APP.PY FILE ---")

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pymongo import MongoClient
from config import Config
import os

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
        # Establish connection to MongoDB
        mongo_uri = app.config['MONGO_URI']
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable not set.")
            
        client = MongoClient(mongo_uri)
        
        # We'll use the database name 'servesmart'
        db = client.servesmart
        
        # Test the connection
        db.command('ping')
        print("MongoDB connection successful!")

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        db = None

    bcrypt.init_app(app)
    login_manager.init_app(app)

    # --- THIS IS THE CORRECTED PART ---
    # We import 'routes' here, inside the function, to avoid the circular import.
    with app.app_context():
        from routes import routes
        app.register_blueprint(routes)

    return app

# This part creates the app instance for Vercel and local execution
app = create_app()

