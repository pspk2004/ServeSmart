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
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register the blueprint for routes
    from routes import routes
    app.register_blueprint(routes)

    # --- Self-initializing database logic ---
    with app.app_context():
        from models import User, Schedule
        
        db.create_all()

        if User.query.filter_by(roll_number='admin').first() is None:
            hashed_password = bcrypt.generate_password_hash('adminpass').decode('utf-8')
            admin = User(name='Admin User', roll_number='admin', password=hashed_password, is_admin=True, points=9999)
            db.session.add(admin)
        
        if Schedule.query.count() == 0:
            print("Meal schedule not found. Seeding database with new menu...")
            # Costs are placeholders and can be edited via the admin panel.
            schedule_items = [
                # Monday
                Schedule(day_of_week='Monday', meal_type='Breakfast', item_name='Vada Pav, Puttu, Channa Curry, Fried Chillies, Onions, Green Chutney, Red Powdered Chutney, Bread, Jam, Butter, Tea, Milk, Banana', cost=35.00),
                Schedule(day_of_week='Monday', meal_type='Lunch', item_name='Jeera Rice, White Rice, Roti, Potato curry, Mulaku Kondattam, Rajma Curry, Fryums, Pulissery, Curd, Salad, Fruit', cost=55.00),
                Schedule(day_of_week='Monday', meal_type='Snacks', item_name='Bhelpuri, Bread, Jam, Butter, Tea, Milk', cost=25.00),
                Schedule(day_of_week='Monday', meal_type='Dinner', item_name='Rice, Roti, Soya chunk curry, Beetroot Dry, Palak Dal tadka, Cabbage chutney, Pepper Rasam, Chips, Curd, Salad, Sweet: Ada Payasam', cost=50.00),
                # Tuesday
                Schedule(day_of_week='Tuesday', meal_type='Breakfast', item_name='Idli, Masala Idli, Punugulu, Sambar, Groundnut Chutney, Tomato Chutney, Bread, Jam, Butter, Coffee, Milk', cost=35.00),
                Schedule(day_of_week='Tuesday', meal_type='Lunch', item_name='Rice, Roti, Chole curry, Onion Dal Tadka, Ivy gourd chutney, Cabbage carrot Thoran, Salad, Curd, Fryums, Drink: Sweet Lassi', cost=55.00),
                Schedule(day_of_week='Tuesday', meal_type='Snacks', item_name='Masala Puri chaat, Bread, Jam, Butter, Tea, Milk', cost=25.00),
                Schedule(day_of_week='Tuesday', meal_type='Dinner', item_name='Rice, Roti, Egg Curry, Dal tadka, Vanpayar Aloo Curry, Tomato rasam, Curd, Papad, Salad, Drink: Grape Drink', cost=50.00),
                # Wednesday
                Schedule(day_of_week='Wednesday', meal_type='Breakfast', item_name='Masala uthappam, Medu vada, Sambar, Coconut Chutney, Bread, Jam, Butter, Coffee, Banana, Milk', cost=35.00),
                Schedule(day_of_week='Wednesday', meal_type='Lunch', item_name='Rice, Roti, Palak Dal tadka, Crunchy Bhindi Fry, Rasam, Papad, Curd, Salad, Banana, Drink: Buttermilk', cost=55.00),
                Schedule(day_of_week='Wednesday', meal_type='Snacks', item_name='Peanuts chaat, Bread, Jam, Butter, Tea, Milk', cost=25.00),
                Schedule(day_of_week='Wednesday', meal_type='Dinner', item_name='Fried rice, Roti, Kadai Paneer, Chilli chicken, Onion Chilli Raita, Drink: Passion Fruit drink', cost=60.00),
                # Thursday
                Schedule(day_of_week='Thursday', meal_type='Breakfast', item_name='Pav Bhaji, Lemons, Onions, Uggani(Puffed rice), Roasted chana Podi, Bread, Jam, Butter, Banana, Tea, Milk', cost=35.00),
                Schedule(day_of_week='Thursday', meal_type='Lunch', item_name='Roti, Rice, Egg Bhurji, Mixed Vegetable Kurma, Tomato Dal tadka Chips, Curd, Salad, Rasam, Drink: Buttermilk', cost=55.00),
                Schedule(day_of_week='Thursday', meal_type='Snacks', item_name='Veg Noodles, Bread, Jam, Butter, Tea, Milk', cost=25.00),
                Schedule(day_of_week='Thursday', meal_type='Dinner', item_name='Rice, Roti, Raw banana stir fry, Radish Chutney, Spicy Dal Tadka, Rasam, Chips, Curd, Salad, Sweet: Vermicelli Payasam', cost=50.00),
                # Friday
                Schedule(day_of_week='Friday', meal_type='Breakfast', item_name='Idli, Masala Idli, Medu Vada, Groundnut Chutney, Tomato chutney, Sambar, Bread, Jam, Butter, Coffee, Milk', cost=35.00),
                Schedule(day_of_week='Friday', meal_type='Lunch', item_name='Rice, Tomato Rice, Roti, Beans and carrot thoran, Sambar, Salad, curd, Chips, chana masala, Seasonal Fruits', cost=55.00),
                Schedule(day_of_week='Friday', meal_type='Snacks', item_name='Kozhukkatta, Bread, Jam, Butter, Tea, Milk', cost=25.00),
                Schedule(day_of_week='Friday', meal_type='Dinner', item_name='White Rice, Tawa Pulao, Roti, Chicken Masala, paneer masala, curd, Vegetable Raita, Salad, Drink: Lychee drink', cost=60.00),
                # Saturday
                Schedule(day_of_week='Saturday', meal_type='Breakfast', item_name='Normal Upma, Vermicelli upma, Sprouts, Groundnut Chutney, Mango Pickle, Bread, Jam, Butter, Banana, Coffee, Milk', cost=35.00),
                Schedule(day_of_week='Saturday', meal_type='Lunch', item_name='Rice, Roti, Kerala Rice, Ivy gourd fry, Onam Koottukari, Parippu Dal, Beetroot Pachadi, Bitter Gourd Kondattam, Papad, Curd, Salad, Drink: Buttermilk', cost=55.00),
                Schedule(day_of_week='Saturday', meal_type='Snacks', item_name='Onion Vada, Bread, Jam, Butter, Tea, Milk', cost=25.00),
                Schedule(day_of_week='Saturday', meal_type='Dinner', item_name='Roti, Rice, Rasam, Potato Roast, Horse Gram Chutney, Onion Dal tadka, curd, Salad, Fryums, Drink: Lemon Sharbat', cost=50.00),
                # Sunday
                Schedule(day_of_week='Sunday', meal_type='Breakfast', item_name='Puri Masala, Pongal, Groundnut chutney, Banana, Boiled Egg, Sprouts, Bread, Jam, Tea, Milk', cost=40.00),
                Schedule(day_of_week='Sunday', meal_type='Lunch', item_name='Rice, Roti, Aloo Bhindi dry, Tomato Dal tadka, Curd, Salad, Coriander, Tomato chutney, Chips, Drink: Sweet Lassi', cost=55.00),
                Schedule(day_of_week='Sunday', meal_type='Snacks', item_name='Mirchi Bajji/cream bun, Bread, Jam, Butter, Tea, Milk', cost=25.00),
                Schedule(day_of_week='Sunday', meal_type='Dinner', item_name='Chicken Biryani, Paneer Biryani, Veg Gravy, Chicken Gravy, Boondi Raita, Onion Chilli Raita, papad, Salad, Drink: Rooh Afza', cost=65.00),
            ]
            db.session.bulk_save_objects(schedule_items)
            print("Meal schedule seeded.")
        
        db.session.commit()
        print("Database initialization check complete.")

    return app

# This line is the entry point for Vercel
app = create_app()