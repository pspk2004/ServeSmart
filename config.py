import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-default-secret-key'
    # We only need one variable for MongoDB!
    MONGO_URI = os.environ.get('MONGO_URI')