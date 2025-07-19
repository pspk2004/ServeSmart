from flask_login import UserMixin
from app import login_manager, db
from bson.objectid import ObjectId # Import ObjectId

@login_manager.user_loader
def load_user(user_id):
    """Loads a user from the database given their ID."""
    # MongoDB uses _id as an ObjectId, so we need to convert the string ID back
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

class User(UserMixin):
    """User model for Flask-Login."""
    def __init__(self, user_data):
        self.id = str(user_data['_id']) # Store ID as a string
        self.roll_number = user_data['roll_number']
        self.name = user_data['name']
        self.password = user_data['password']
        self.is_admin = user_data.get('is_admin', False)
        self.points = user_data.get('points', 1000.00)
        self.opt_out_month = user_data.get('opt_out_month', None)