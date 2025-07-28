import uuid
from datetime import date
from decimal import Decimal
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import joinedload # Make sure this import is here
from app import db, bcrypt
from models import User, Schedule, Registration
from utils import generate_qr_code

routes = Blueprint('routes', __name__)

# --- Main and Auth Routes (No changes) ---
@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('routes.dashboard'))
    if request.method == 'POST':
        name, roll_number, password = request.form['name'], request.form['roll_number'], request.form['password']
        if User.query.filter_by(roll_number=roll_number).first():
            flash('Roll number already exists. Please log in.', 'danger')
            return redirect(url_for('routes.register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, roll_number=roll_number, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('routes.dashboard'))
    if request.method == 'POST':
        roll_number, password = request.form['roll_number'], request.form['password']
        user = User.query.filter_by(roll_number=roll_number).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('routes.dashboard'))
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
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule_items = Schedule.query.all()
    schedule = sorted(schedule_items, key=lambda x: day_order.index(x.day_of_week))
    
    # EAGER LOADING: Pre-load the related 'meal' data for each registration.
    active_tokens = Registration.query.options(joinedload(Registration.meal)).filter_by(
        user_id=current_user.id, 
        registration_date=date.today(), 
        is_used=False
    ).all()

    for token in active_tokens:
        token.qr_code = generate_qr_code(token.token)
        
    return render_template('student_dashboard.html', schedule=schedule, user_data=current_user, active_tokens=active_tokens)

@routes.route('/register_meal', methods=['POST'])
@login_required
def register_meal():
    try:
        schedule_id = request.form.get('schedule_id')
        if not schedule_id: return jsonify({'success': False, 'message': 'Meal ID not provided.'}), 400
        meal = Schedule.query.get(int(schedule_id))
        if not meal: return jsonify({'success': False, 'message': 'Meal not found.'}), 404
        if current_user.points < meal.cost: return jsonify({'success': False, 'message': 'Insufficient points.'})
        
        token_str = str(uuid.uuid4())
        current_user.points -= meal.cost
        
        new_registration = Registration(token=token_str, user_id=current_user.id, schedule_id=meal.id, registration_date=date.today())
        db.session.add(new_registration)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Meal registered successfully!'})
    except Exception as e:
        db.session.rollback()
        print(f"Error in /register_meal: {e}")
        return jsonify({'success': False, 'message': 'A server error occurred.'}), 500

@routes.route('/meal_history')
@login_required
def meal_history():
    # EAGER LOADING: Pre-load the related 'meal' data.
    registrations = Registration.query.options(joinedload(Registration.meal)).filter_by(user_id=current_user.id).order_by(Registration.created_at.desc()).all()
    history = [{"created_at": reg.created_at.strftime('%Y-%m-%d'), "meal_details": {"item_name": reg.meal.item_name, "cost": float(reg.meal.cost)}, "is_used": reg.is_used} for reg in registrations]
    return jsonify(history)

# --- Admin Routes ---
@routes.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin: return redirect(url_for('routes.student_dashboard'))
    
    # --- THIS IS THE FINAL FIX ---
    # EAGER LOADING: Pre-load BOTH the related 'meal' and 'student' (User) data.
    # The template needs both reg.meal.item_name and reg.student.name.
    registrations = Registration.query.options(
        joinedload(Registration.meal), 
        joinedload(Registration.student)
    ).filter_by(registration_date=date.today()).order_by(Registration.created_at.desc()).all()
    
    return render_template('admin_dashboard.html', registrations=registrations)

@routes.route('/verify_token', methods=['POST'])
@login_required
def verify_token():
    if not current_user.is_admin: return jsonify({'success': False, 'message': 'Unauthorized'})
    token = request.form.get('token', '').strip()
    if not token: return jsonify({'success': False, 'message': 'Token cannot be empty.'})
    registration = Registration.query.filter_by(token=token, registration_date=date.today(), is_used=False).first()
    if registration:
        registration.is_used = True
        db.session.commit()
        return jsonify({'success': True, 'message': 'Token verified successfully!'})
    else:
        if Registration.query.filter_by(token=token, registration_date=date.today()).first():
            return jsonify({'success': False, 'message': 'This token has already been used.'})
        else:
            return jsonify({'success': False, 'message': 'Invalid or expired token.'})