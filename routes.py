import uuid
from datetime import date, datetime
from decimal import Decimal
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from models import User, Schedule, Registration
from utils import generate_qr_code

routes = Blueprint('routes', __name__)

# --- Main and Auth Routes ---
@routes.route('/')
def index(): return render_template('index.html')

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('routes.dashboard'))
    if request.method == 'POST':
        name, roll_number, password = request.form['name'], request.form['roll_number'], request.form['password']
        if User.query.filter_by(roll_number=roll_number).first():
            flash('Roll number already exists. Please log in.', 'danger'); return redirect(url_for('routes.register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, roll_number=roll_number, password=hashed_password)
        db.session.add(new_user); db.session.commit()
        flash('Your account has been created! You can now log in.', 'success'); return redirect(url_for('routes.login'))
    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('routes.dashboard'))
    if request.method == 'POST':
        roll_number, password = request.form['roll_number'], request.form['password']
        user = User.query.filter_by(roll_number=roll_number).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True); return redirect(url_for('routes.dashboard'))
        else:
            flash('Login unsuccessful. Please check roll number and password.', 'danger')
    return render_template('login.html')

@routes.route('/logout')
def logout(): logout_user(); return redirect(url_for('routes.index'))

@routes.route('/dashboard')
@login_required
def dashboard(): return redirect(url_for('routes.admin_dashboard')) if current_user.is_admin else redirect(url_for('routes.student_dashboard'))


# --- Student Routes ---
@routes.route('/student')
@login_required
def student_dashboard():
    # Feature: Show today's meals only
    today_day_name = datetime.now().strftime('%A')
    todays_schedule = Schedule.query.filter_by(day_of_week=today_day_name).order_by('id').all()
    
    # Get IDs of meals the student has already registered for today
    todays_registrations = Registration.query.filter_by(user_id=current_user.id, registration_date=date.today()).all()
    registered_meal_ids = {reg.schedule_id for reg in todays_registrations}
    
    active_tokens = [reg for reg in todays_registrations if not reg.is_used]
    for token in active_tokens:
        token.qr_code = generate_qr_code(token.token)
        token.meal = Schedule.query.get(token.schedule_id)
        
    return render_template('student_dashboard.html', 
                           schedule=todays_schedule, 
                           user_data=current_user, 
                           active_tokens=active_tokens,
                           registered_meal_ids=registered_meal_ids)

@routes.route('/register_meal', methods=['POST'])
@login_required
def register_meal():
    try:
        schedule_id = request.form.get('schedule_id')
        if not schedule_id: return jsonify({'success': False, 'message': 'Meal ID not provided.'}), 400
        meal = Schedule.query.get(int(schedule_id))
        if not meal: return jsonify({'success': False, 'message': 'Meal not found.'}), 404
        
        # Feature: Prevent duplicate registrations
        existing_registration = Registration.query.filter_by(user_id=current_user.id, schedule_id=meal.id, registration_date=date.today()).first()
        if existing_registration: return jsonify({'success': False, 'message': 'You have already registered for this meal today.'})
            
        if current_user.points < meal.cost: return jsonify({'success': False, 'message': 'Insufficient points.'})
        
        token_str = str(uuid.uuid4())
        current_user.points -= meal.cost
        
        new_registration = Registration(token=token_str, user_id=current_user.id, schedule_id=meal.id, registration_date=date.today())
        db.session.add(new_registration); db.session.commit()
        
        qr_code_b64 = generate_qr_code(token_str)
        return jsonify({'success': True, 'message': 'Meal registered successfully!', 'token': token_str, 'qr_code': qr_code_b64})
    except Exception as e:
        db.session.rollback(); print(f"Error in /register_meal: {e}")
        return jsonify({'success': False, 'message': 'A server error occurred.'}), 500

@routes.route('/meal_history')
@login_required
def meal_history():
    registrations = Registration.query.filter_by(user_id=current_user.id).order_by(Registration.created_at.desc()).all()
    for reg in registrations: reg.meal = Schedule.query.get(reg.schedule_id)
    history = [{"created_at": reg.created_at.strftime('%Y-%m-%d'), "meal_details": {"item_name": reg.meal.item_name, "cost": float(reg.meal.cost)}, "is_used": reg.is_used} for reg in registrations]
    return jsonify(history)


# --- Admin Routes ---
@routes.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin: return redirect(url_for('routes.student_dashboard'))
    registrations = Registration.query.filter_by(registration_date=date.today()).order_by(Registration.created_at.desc()).all()
    for reg in registrations:
        reg.student = User.query.get(reg.user_id)
        reg.meal = Schedule.query.get(reg.schedule_id)
    return render_template('admin_dashboard.html', registrations=registrations)

@routes.route('/verify_token', methods=['POST'])
@login_required
def verify_token():
    if not current_user.is_admin: return jsonify({'success': False, 'message': 'Unauthorized'})
    token = request.form.get('token', '').strip()
    if not token: return jsonify({'success': False, 'message': 'Token cannot be empty.'})
    registration = Registration.query.filter_by(token=token, registration_date=date.today(), is_used=False).first()
    if registration:
        registration.is_used = True; db.session.commit()
        return jsonify({'success': True, 'message': 'Token verified successfully!'})
    else:
        if Registration.query.filter_by(token=token, registration_date=date.today()).first():
            return jsonify({'success': False, 'message': 'This token has already been used.'})
        else:
            return jsonify({'success': False, 'message': 'Invalid or expired token.'})

# --- ADVANCED ADMIN FEATURES ---
@routes.route('/admin/students')
@login_required
def manage_students():
    if not current_user.is_admin: return redirect(url_for('routes.student_dashboard'))
    students = User.query.filter_by(is_admin=False).order_by(User.roll_number).all()
    return render_template('admin_students.html', students=students)

@routes.route('/admin/schedule')
@login_required
def manage_schedule():
    if not current_user.is_admin: return redirect(url_for('routes.student_dashboard'))
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule = sorted(Schedule.query.all(), key=lambda x: day_order.index(x.day_of_week))
    return render_template('admin_schedule.html', schedule=schedule)

@routes.route('/admin/schedule/add', methods=['GET', 'POST'])
@login_required
def add_meal():
    if not current_user.is_admin: return redirect(url_for('routes.student_dashboard'))
    if request.method == 'POST':
        new_meal = Schedule(day_of_week=request.form['day_of_week'], meal_type=request.form['meal_type'], item_name=request.form['item_name'], cost=request.form['cost'])
        db.session.add(new_meal); db.session.commit()
        flash('New meal has been added!', 'success')
        return redirect(url_for('routes.manage_schedule'))
    return render_template('admin_meal_form.html', title='Add New Meal', meal=None)

@routes.route('/admin/schedule/edit/<int:meal_id>', methods=['GET', 'POST'])
@login_required
def edit_meal(meal_id):
    if not current_user.is_admin: return redirect(url_for('routes.student_dashboard'))
    meal = Schedule.query.get_or_404(meal_id)
    if request.method == 'POST':
        meal.day_of_week, meal.meal_type, meal.item_name, meal.cost = request.form['day_of_week'], request.form['meal_type'], request.form['item_name'], request.form['cost']
        db.session.commit()
        flash('Meal has been updated!', 'success')
        return redirect(url_for('routes.manage_schedule'))
    return render_template('admin_meal_form.html', title='Edit Meal', meal=meal)

@routes.route('/admin/schedule/delete/<int:meal_id>', methods=['POST'])
@login_required
def delete_meal(meal_id):
    if not current_user.is_admin: return redirect(url_for('routes.student_dashboard'))
    meal = Schedule.query.get_or_404(meal_id)
    db.session.delete(meal); db.session.commit()
    flash('Meal has been deleted!', 'success')
    return redirect(url_for('routes.manage_schedule'))