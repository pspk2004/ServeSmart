# This is the complete, corrected routes.py file.
# Replace the entire contents of your existing file with this.

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from bson.objectid import ObjectId
from app import db, bcrypt
from models import User
from utils import generate_qr_code
import uuid
from datetime import datetime
from app import db, bcrypt, INITIAL_DB_ERROR

routes = Blueprint('routes', __name__)

# --- Helper function to pre-populate data ---
def initialize_mess_data():
    if not db.users.find_one({"roll_number": "admin"}):
        hashed_password = bcrypt.generate_password_hash('adminpass').decode('utf-8')
        db.users.insert_one({
            "roll_number": "admin", "name": "Admin User", "password": hashed_password,
            "is_admin": True, "points": 9999
        })
        print("Admin user created.")

    if db.schedule.count_documents({}) == 0:
        schedule_items = [
            {'day_of_week': 'Monday', 'meal_type': 'Breakfast', 'item_name': 'Aloo Paratha', 'cost': 30.00},
            {'day_of_week': 'Monday', 'meal_type': 'Lunch', 'item_name': 'Rajma Chawal', 'cost': 50.00},
            {'day_of_week': 'Monday', 'meal_type': 'Dinner', 'item_name': 'Shahi Paneer, Naan', 'cost': 60.00},
            {'day_of_week': 'Tuesday', 'meal_type': 'Breakfast', 'item_name': 'Idli Sambar', 'cost': 25.00},
            {'day_of_week': 'Tuesday', 'meal_type': 'Lunch', 'item_name': 'Lemon Rice', 'cost': 45.00},
            {'day_of_week': 'Tuesday', 'meal_type': 'Dinner', 'item_name': 'Chole Bhature', 'cost': 55.00},
            {'day_of_week': 'Wednesday', 'meal_type': 'Breakfast', 'item_name': 'Poha', 'cost': 20.00},
            {'day_of_week': 'Wednesday', 'meal_type': 'Lunch', 'item_name': 'Veg Biryani', 'cost': 50.00},
            {'day_of_week': 'Wednesday', 'meal_type': 'Dinner', 'item_name': 'Dal Makhani, Roti', 'cost': 55.00},
            {'day_of_week': 'Thursday', 'meal_type': 'Breakfast', 'item_name': 'Dosa', 'cost': 30.00},
            {'day_of_week': 'Thursday', 'meal_type': 'Lunch', 'item_name': 'Kadhi Pakoda, Rice', 'cost': 45.00},
            {'day_of_week': 'Thursday', 'meal_type': 'Dinner', 'item_name': 'Matar Paneer, Roti', 'cost': 60.00},
            {'day_of_week': 'Friday', 'meal_type': 'Breakfast', 'item_name': 'Upma', 'cost': 20.00},
            {'day_of_week': 'Friday', 'meal_type': 'Lunch', 'item_name': 'Veg Fried Rice', 'cost': 50.00},
            {'day_of_week': 'Friday', 'meal_type': 'Dinner', 'item_name': 'Mix Veg, Roti', 'cost': 55.00},
            {'day_of_week': 'Saturday', 'meal_type': 'Breakfast', 'item_name': 'Sandwich', 'cost': 25.00},
            {'day_of_week': 'Saturday', 'meal_type': 'Lunch', 'item_name': 'Special Thali', 'cost': 70.00},
            {'day_of_week': 'Saturday', 'meal_type': 'Dinner', 'item_name': 'Pav Bhaji', 'cost': 55.00},
            {'day_of_week': 'Sunday', 'meal_type': 'Breakfast', 'item_name': 'Puri Sabji', 'cost': 35.00},
            {'day_of_week': 'Sunday', 'meal_type': 'Lunch', 'item_name': 'Sunday Special Lunch', 'cost': 75.00},
            {'day_of_week': 'Sunday', 'meal_type': 'Dinner', 'item_name': 'Paneer Butter Masala, Naan', 'cost': 65.00},
        ]
        db.schedule.insert_many(schedule_items)
        print("Meal schedule created.")

# --- Main and Auth Routes ---
@routes.route('/')
def index():
    initialize_mess_data()
    return render_template('index.html')

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('routes.dashboard'))
    if request.method == 'POST':
        name, roll_number, password = request.form['name'], request.form['roll_number'], request.form['password']
        if db.users.find_one({"roll_number": roll_number}):
            flash('Roll number already exists. Please log in.', 'danger')
            return redirect(url_for('routes.register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.users.insert_one({"name": name, "roll_number": roll_number, "password": hashed_password, "is_admin": False, "points": 1000.00})
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('routes.dashboard'))
    if request.method == 'POST':
        roll_number, password = request.form['roll_number'], request.form['password']
        user_data = db.users.find_one({"roll_number": roll_number})
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.dashboard'))
        else:
            flash('Login unsuccessful. Please check roll number and password.', 'danger')
    return render_template('login.html')

@routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@routes.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('routes.admin_dashboard')) if current_user.is_admin else redirect(url_for('routes.student_dashboard'))

# --- Student Routes ---
@routes.route('/student')
@login_required
def student_dashboard():
    user_data = db.users.find_one({"_id": ObjectId(current_user.id)})
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule_cursor = db.schedule.find()
    schedule = sorted(list(schedule_cursor), key=lambda x: day_order.index(x['day_of_week']))
    
    # THE UNIFIED LOGIC: Use a consistent UTC date string
    today_str = datetime.utcnow().strftime('%Y-%m-%d')
    active_tokens_cursor = db.registrations.find({"user_id": ObjectId(current_user.id), "registration_date": today_str, "is_used": False})
    active_tokens = list(active_tokens_cursor)
    for token in active_tokens:
        token['qr_code'] = generate_qr_code(token['token'])

    return render_template('student_dashboard.html', schedule=schedule, user_data=user_data, active_tokens=active_tokens)

@routes.route('/register_meal', methods=['POST'])
@login_required
def register_meal():
    schedule_id = request.form.get('schedule_id')
    meal = db.schedule.find_one({"_id": ObjectId(schedule_id)})
    user = db.users.find_one({"_id": ObjectId(current_user.id)})
    if user['points'] < meal['cost']:
        return jsonify({'success': False, 'message': 'Insufficient points.'})
    token = str(uuid.uuid4())
    
    # THE UNIFIED LOGIC: Store the consistent UTC date string
    today_str = datetime.utcnow().strftime('%Y-%m-%d')
    
    db.users.update_one({"_id": ObjectId(current_user.id)}, {"$inc": {"points": -meal['cost']}})
    db.registrations.insert_one({
        "user_id": ObjectId(current_user.id), "user_roll_number": user['roll_number'], "user_name": user['name'],
        "schedule_id": meal['_id'], "meal_details": {"item_name": meal['item_name'], "cost": meal['cost']},
        "registration_date": today_str, "token": token, "is_used": False, "created_at": datetime.utcnow()
    })
    return jsonify({'success': True, 'message': 'Meal registered successfully!', 'qr_code': generate_qr_code(token), 'token': token})

@routes.route('/meal_history')
@login_required
def meal_history():
    history_cursor = db.registrations.find({"user_id": ObjectId(current_user.id)}).sort("created_at", -1)
    history = []
    for item in list(history_cursor):
        item['_id'], item['user_id'], item['schedule_id'] = str(item['_id']), str(item['user_id']), str(item['schedule_id'])
        if 'created_at' in item and isinstance(item['created_at'], datetime):
            item['created_at'] = {'$date': item['created_at'].isoformat()}
        history.append(item)
    return jsonify(history)

# --- Admin Routes ---
@routes.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin: return redirect(url_for('routes.student_dashboard'))
    today_str = datetime.utcnow().strftime('%Y-%m-%d')
    registrations_cursor = db.registrations.find({"registration_date": today_str}).sort("created_at", -1)
    return render_template('admin_dashboard.html', registrations=list(registrations_cursor))

@routes.route('/verify_token', methods=['POST'])
@login_required
def verify_token():
    if not current_user.is_admin: return jsonify({'success': False, 'message': 'Unauthorized'})
    token = request.form.get('token', '').strip()
    if not token: return jsonify({'success': False, 'message': 'Token cannot be empty.'})
    
    # THE UNIFIED LOGIC: Use the consistent UTC date string for verification
    today_str = datetime.utcnow().strftime('%Y-%m-%d')
    
    result = db.registrations.find_one_and_update(
        {"token": token, "registration_date": today_str, "is_used": False},
        {"$set": {"is_used": True}}
    )
    if result:
        return jsonify({'success': True, 'message': 'Token verified successfully!'})
    else:
        existing = db.registrations.find_one({"token": token, "registration_date": today_str})
        if existing:
            return jsonify({'success': False, 'message': 'This token has already been used.'})
        else:
            return jsonify({'success': False, 'message': 'Invalid or expired token.'})  

            # In routes.py, add this entire new function at the end of the file.

@routes.route('/health-check-12345')
def health_check():
    """
    Displays the initial database connection error if it exists.
    """
    # --- THIS IS THE NEW LOGIC ---
    if INITIAL_DB_ERROR:
        # If our global error variable has something in it, display it.
        # This is the root cause of the Internal Server Error.
        return f"""
            <h1>The Root Cause of the Error Has Been Found</h1>
            <p>The application could not connect to the database at startup.</p>
            <h2>The specific connection error was:</h2>
            <pre style='background-color: #f0f0f0; padding: 15px; border: 1px solid #ccc; white-space: pre-wrap; word-wrap: break-word;'>{INITIAL_DB_ERROR}</pre>
            <p>This is the final error message we need to solve the problem.</p>
        """
    
    # If there was no initial error, check if the db connection is okay.
    if db is None:
        return "<h1>Error: Database object is None, but no initial connection error was recorded.</h1>"

    # If everything looks okay, try to ping the database.
    try:
        db.command('ping')
        return "<h1>Success! The database connection is OK.</h1>"
    except Exception as e:
        return f"<h1>Ping Failed! The connection was established but is now broken. Error: {e}</h1>"
