import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Get the secret key from environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Get the database URL that Vercel automatically provides
    db_url = os.environ.get('POSTGRES_URL')
    
    # --- THIS IS THE FINAL FIX ---
    # Check if the URL starts with the problematic prefix
    if db_url and db_url.startswith("postgres://"):
        # Replace it with the correct prefix that psycopg2 expects
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    # Assign the corrected URL to the configuration variable
    SQLALCHEMY_DATABASE_URI = db_url
    
    # This is recommended to disable a feature we don't need
    SQLALCHEMY_TRACK_MODIFICATIONS = False