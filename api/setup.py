# This is a Vercel Serverless Function
from http.server import BaseHTTPRequestHandler
import os
# We need to add the parent directory to the path to import our app
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import User, Schedule
from flask_bcrypt import Bcrypt

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        app = create_app()
        bcrypt = Bcrypt(app)
        
        output = "Starting database setup...\n"
        with app.app_context():
            try:
                output += "Creating all database tables...\n"
                db.create_all()
                output += "Tables created successfully.\n"

                if User.query.filter_by(roll_number='admin').first() is None:
                    output += "Admin user not found, creating one...\n"
                    hashed_password = bcrypt.generate_password_hash('adminpass').decode('utf-8')
                    admin = User(name='Admin User', roll_number='admin', password=hashed_password, is_admin=True, points=9999)
                    db.session.add(admin)
                    output += "Admin user added.\n"
                else:
                    output += "Admin user already exists.\n"

                if Schedule.query.count() == 0:
                    output += "Schedule not found, creating one...\n"
                    # (Shortened schedule for brevity)
                    schedule_items = [Schedule(day_of_week='Monday', meal_type='Breakfast', item_name='Aloo Paratha', cost=30.00)]
                    db.session.bulk_save_objects(schedule_items)
                    output += "Schedule added.\n"
                else:
                    output += "Schedule already exists.\n"
                    
                db.session.commit()
                output += "Database initialization complete!"
                
                self.send_response(200)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))
            
            except Exception as e:
                output += f"\nAN ERROR OCCURRED:\n{str(e)}"
                self.send_response(500)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))
        return