#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# This single command runs a python script to set up the database.
# It creates an app context, creates tables, and seeds the initial data.
python -c 'from app import create_app, db; from models import User, Schedule; from flask_bcrypt import Bcrypt; app = create_app(); app.app_context().push(); bcrypt = Bcrypt(app); db.create_all(); \
    admin = User.query.filter_by(roll_number="admin").first(); \
    if not admin: \
        hashed_password = bcrypt.generate_password_hash("adminpass").decode("utf-8"); \
        admin = User(name="Admin User", roll_number="admin", password=hashed_password, is_admin=True, points=9999); \
        db.session.add(admin); \
    if Schedule.query.count() == 0: \
        schedule_items = [ \
            Schedule(day_of_week="Monday", meal_type="Breakfast", item_name="Aloo Paratha", cost=30.00), \
            Schedule(day_of_week="Monday", meal_type="Lunch", item_name="Rajma Chawal", cost=50.00), \
            Schedule(day_of_week="Monday", meal_type="Dinner", item_name="Shahi Paneer, Naan", cost=60.00), \
            Schedule(day_of_week="Tuesday", meal_type="Breakfast", item_name="Idli Sambar", cost=25.00), \
            Schedule(day_of_week="Tuesday", meal_type="Lunch", item_name="Lemon Rice", cost=45.00), \
            Schedule(day_of_week="Tuesday", meal_type="Dinner", item_name="Chole Bhature", cost=55.00), \
            Schedule(day_of_week="Wednesday", meal_type="Breakfast", item_name="Poha", cost=20.00), \
            Schedule(day_of_week="Wednesday", meal_type="Lunch", item_name="Veg Biryani", cost=50.00), \
            Schedule(day_of_week="Wednesday", meal_type="Dinner", item_name="Dal Makhani, Roti", cost=55.00), \
            Schedule(day_of_week="Thursday", meal_type="Breakfast", item_name="Dosa", cost=30.00), \
            Schedule(day_of_week="Thursday", meal_type="Lunch", item_name="Kadhi Pakoda, Rice", cost=45.00), \
            Schedule(day_of_week="Thursday", meal_type="Dinner", item_name="Matar Paneer, Roti", cost=60.00), \
            Schedule(day_of_week="Friday", meal_type="Breakfast", item_name="Upma", cost=20.00), \
            Schedule(day_of_week="Friday", meal_type="Lunch", item_name="Veg Fried Rice", cost=50.00), \
            Schedule(day_of_week="Friday", meal_type="Dinner", item_name="Mix Veg, Roti", cost=55.00), \
            Schedule(day_of_week="Saturday", meal_type="Breakfast", item_name="Sandwich", cost=25.00), \
            Schedule(day_of_week="Saturday", meal_type="Lunch", item_name="Special Thali", cost=70.00), \
            Schedule(day_of_week="Saturday", meal_type="Dinner", item_name="Pav Bhaji", cost=55.00), \
            Schedule(day_of_week="Sunday", meal_type="Breakfast", item_name="Puri Sabji", cost=35.00), \
            Schedule(day_of_week="Sunday", meal_type="Lunch", item_name="Sunday Special Lunch", cost=75.00), \
            Schedule(day_of_week="Sunday", meal_type="Dinner", item_name="Paneer Butter Masala, Naan", cost=65.00), \
        ]; \
        db.session.bulk_save_objects(schedule_items); \
    db.session.commit(); print("Database setup complete.")'