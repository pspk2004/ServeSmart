from app import create_app

# The create_app function from app.py is called to create the Flask app instance.
# Vercel will automatically find and serve this 'app' object.
app = create_app()