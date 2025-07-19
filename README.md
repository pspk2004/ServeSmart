ServeSmart - A Modern College Mess Management System
ServeSmart is a complete, end-to-end mess management system built for colleges and hostels. It provides a seamless digital experience for both students and mess administrators, handling everything from meal registration and real-time QR code verification to point tracking and user management.
This project is built with a robust Python Flask backend, a dynamic HTML/CSS/JavaScript frontend, and a scalable NoSQL database (MongoDB). It is designed for easy deployment on modern cloud platforms.
🚀 Core Features
🎓 For Students
Simple Registration & Login: Secure authentication using college roll numbers.
Point-Based System: Students start with a point balance that is used for meal registrations.
One-Click Meal Registration: Register for any meal with a single button click from the weekly menu.
Active Token Display: A dedicated section on the dashboard prominently displays all unused QR codes for the current day. A student can never lose their token.
Meal & Point History: Track a complete history of all registered meals and their status (Used/Not Used).
🧑‍💼 For Administrators
Secure Admin Login: A separate, secure login for mess administrators (admin / adminpass).
Live QR Code Scanner: A real-time, camera-based QR code scanner for instant and error-free token verification.
Manual Verification Backup: An option to manually type in a token ID if the scanner fails.
Daily Registration Overview: A dashboard that lists all students who have registered for meals on the current day and their token status.
🛠️ Tech Stack
Backend: Python with the Flask web framework.
Frontend: HTML5, CSS3, and JavaScript with the Bootstrap 5 framework for a clean, responsive UI.
Database: MongoDB (designed to be hosted on MongoDB Atlas or another cloud provider).
QR Code Generation: qrcode Python library.
QR Code Scanning: html5-qrcode JavaScript library for live camera scanning.
Deployment Target: Vercel.
⚙️ How to Run Locally
Follow these steps to get a copy of the project up and running on your own computer for development and testing.
Prerequisites
Python 3.9+ installed on your computer.
Git installed on your computer.
A code editor like Visual Studio Code.
A free MongoDB Atlas account.
Step 1: Set Up the Free MongoDB Database
This project requires a cloud-hosted MongoDB database. We will use MongoDB Atlas's free tier.
Create a Free Cluster: Log in to MongoDB Atlas and create a new M0 Sandbox (Free Tier) cluster.
Create a Database User: In your cluster's settings, go to "Security" -> "Database Access".
Click "Add New Database User".
Enter a username (e.g., servesmart_user).
Enter a strong password and save it somewhere safe immediately.
Grant the user the "Read and write to any database" privilege.
Configure Network Access: Go to "Security" -> "Network Access".
Click "Add IP Address".
Select "ALLOW ACCESS FROM ANYWHERE". This will enter 0.0.0.0/0 and is necessary for both local testing and Vercel deployment.
Get Your Connection String: Go back to your database view, click the "Connect" button, and select "Drivers".
A connection string will be displayed. Copy it. It will look like mongodb+srv://<username>:<password>@....
This is your template.
Step 2: Set Up the Project on Your Computer
Get the Code: Open your terminal or command prompt and clone the repository:
Generated bash
git clone https://github.com/YourGitHubUsername/servesmart.git
cd servesmart
Use code with caution.
Bash
Create and Activate a Virtual Environment: This keeps your project's dependencies isolated.
Generated bash
# For Windows (using the 'py' launcher)
py -m venv venv
venv\Scripts\activate

# For macOS / Linux
python3 -m venv venv
source venv/bin/activate
Use code with caution.
Bash
You should see (venv) at the beginning of your terminal prompt.
Install All Required Packages:
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash
Create the Secret .env File: In the main servesmart folder, create a new file named .env. This file will hold your secret credentials and is never uploaded to GitHub.
Open the .env file and add the following lines:
Generated code
# Replace the placeholder text with your real credentials

# Paste your MongoDB connection string here, replacing <password> with your real password.
MONGO_URI="mongodb+srv://servesmart_user:YourRealPasswordHere@your-cluster-address.mongodb.net/?retryWrites=true&w=majority"

# Create a long, random string for Flask's session security.
SECRET_KEY="any-long-random-string-of-characters-goes-here-for-local-development"
Use code with caution.
Step 3: Run the Application!
You are all set! In your terminal (with the virtual environment still active), run the following command:
Generated bash
python run.py
Use code with caution.
Bash
You will see output in your terminal confirming the database connection is successful and the server is running.
Generated code
MongoDB connection successful!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
Use code with caution.
Open your web browser and go to http://127.0.0.1:5000 to use your application.
🚀 Deployment
This application is configured for easy deployment to Vercel.
Push your code to a GitHub repository.
On Vercel, import the project from your GitHub repository.
In the Vercel project settings, add the same MONGO_URI and SECRET_KEY environment variables that you used in your local .env file.
Click "Deploy". Vercel will handle the rest.
