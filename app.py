from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Create extension instances
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    """Creates and configures the Flask application."""
    
    # --- THIS IS THE FIX ---
    # We are explicitly telling Flask where to find the static files.
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    
    app.config.from_object(config_class)
    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register the blueprint for routes
    from routes import routes
    app.register_blueprint(routes)

    # --- THIS IS THE NEW, ROBUST DATABASE SETUP LOGIC ---
    with app.app_context():
        # Import models here to avoid circular import issues
        from models import User, Schedule
        
        # This will create any tables that do not already exist.
        # It is safe to run this every time the app starts.
        db.create_all()

        # Seed the database with the admin user and schedule if they don't exist.
        # This is also safe to run every time.
        if User.query.filter_by(roll_number='admin').first() is None:
            print("Admin user not found. Creating one...")
            hashed_password = bcrypt.generate_password_hash('adminpass').decode('utf-8')
            admin = User(name='Admin User', roll_number='admin', password=hashed_password, is_admin=True, points=9999)
            db.session.add(admin)
            print("Admin user created.")
        
        if Schedule.query.count() == 0:
            print("Meal schedule not found. Seeding database...")
            schedule_items = [
                Schedule(day_of_week='Monday', meal_type='Breakfast', item_name='Aloo Paratha', cost=30.00),
                Schedule(day_of_week='Monday', meal_type='Lunch', item_name='Rajma Chawal', cost=50.00),
                Schedule(day_of_week='Monday', meal_type='Dinner', item_name='Shahi Paneer, Naan', cost=60.00),
                Schedule(day_of_week='Tuesday', meal_type='Breakfast', item_name='Idli Sambar', cost=25.00),
                Schedule(day_of_week='Tuesday', meal_type='Lunch', item_name='Lemon Rice', cost=45.00),
                Schedule(day_of_week='Tuesday', meal_type='Dinner', item_name='Chole Bhature', cost=55.00),
                Schedule(day_of_week='Wednesday', meal_type='Breakfast', item_name='Poha', cost=20.00),
                Schedule(day_of_week='Wednesday', meal_type='Lunch', item_name='Veg Biryani', cost=50.00),
                Schedule(day_of_week='Wednesday', meal_type='Dinner', item_name='Dal Makhani, Roti', cost=55.00),
                Schedule(day_of_week='Thursday', meal_type='Breakfast', item_name='Dosa', cost=30.00),
                Schedule(day_of_week='Thursday', meal_type='Lunch', item_name='Kadhi Pakoda, Rice', cost=45.00),
                Schedule(day_of_week='Thursday', meal_type='Dinner', item_name='Matar Paneer, Roti', cost=60.00),
                Schedule(day_of_week='Friday', meal_type='Breakfast', item_name='Upma', cost=20.00),
                Schedule(day_of_week='Friday', meal_type='Lunch', item_name='Veg Fried Rice', cost=50.00),
                Schedule(day_of_week='Friday', meal_type='Dinner', item_name='Mix Veg, Roti', cost=55.00),
                Schedule(day_of_week='Saturday', meal_type='Breakfast', item_name='Sandwich', cost=25.00),
                Schedule(day_of_week='Saturday', meal_type='Lunch', item_name='Special Thali', cost=70.00),
                Schedule(day_of_week='Saturday', meal_type='Dinner', item_name='Pav Bhaji', cost=55.00),
                Schedule(day_of_week='Sunday', meal_type='Breakfast', item_name='Puri Sabji', cost=35.00),
                Schedule(day_of_week='Sunday', meal_type='Lunch', item_name='Sunday Special Lunch', cost=75.00),
                Schedule(day_of_week='Sunday', meal_type='Dinner', item_name='Paneer Butter Masala, Naan', cost=65.00),
            ]
            db.session.bulk_save_objects(schedule_items)
            print("Meal schedule seeded.")
        
        db.session.commit()
        print("Database initialization check complete.")

    return app

# This line is important for Vercel. It creates the 'app' instance that Vercel looks for.
app = create_app()