# ServeSmart - A Modern College Mess Management System

ServeSmart is a complete, end-to-end mess management system built for colleges and hostels. It provides a seamless digital experience for both students and mess administrators, handling everything from meal registration and real-time QR code verification to point tracking and user management.

This project is built with a robust Python Flask backend, a dynamic HTML/CSS/JavaScript frontend, and a scalable NoSQL database (MongoDB). It is designed for easy deployment on modern cloud platforms.

## 🚀 Core Features

### 🎓 For Students
- **Simple Registration & Login**: Secure authentication using college roll numbers.
- **Point-Based System**: Students start with a point balance that is used for meal registrations.
- **One-Click Meal Registration**: Register for any meal with a single button click from the weekly menu.
- **Active Token Display**: A dedicated section on the dashboard prominently displays all unused QR codes for the current day.
- **Meal & Point History**: Track a complete history of all registered meals and their status (Used/Not Used).

### 🧑‍💼 For Administrators
- **Secure Admin Login**: A separate, secure login for mess administrators (`admin` / `adminpass`).
- **Live QR Code Scanner**: A real-time, camera-based QR code scanner for instant and error-free token verification.
- **Manual Verification Backup**: An option to manually type in a token ID if the scanner fails.
- **Daily Registration Overview**: A dashboard that lists all students who have registered for meals on the current day and their token status.

## 🛠️ Tech Stack
- **Backend**: Python with the Flask web framework.
- **Frontend**: HTML5, CSS3, and JavaScript with Bootstrap 5.
- **Database**: MongoDB (cloud-hosted via MongoDB Atlas).
- **QR Code Generation**: `qrcode` Python library.
- **QR Code Scanning**: `html5-qrcode` JavaScript library.
- **Deployment Target**: Vercel

## ⚙️ How to Run Locally

### Prerequisites
- Python 3.9+
- Git
- Code editor (e.g. VS Code)
- Free MongoDB Atlas account

### Step 1: Set Up MongoDB Atlas
1. Create a Free M0 Cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Add a database user and whitelist access from `0.0.0.0/0`.
3. Get your connection string (e.g. `mongodb+srv://<user>:<password>@cluster0.mongodb.net/...`).

### Step 2: Clone and Set Up the Project

```bash
git clone https://github.com/YourGitHubUsername/servesmart.git
cd servesmart
```

#### Create Virtual Environment

Windows:
```bash
py -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Requirements
```bash
pip install -r requirements.txt
```

#### Create `.env` file
Create a `.env` file in the root directory and paste the following:

```env
MONGO_URI="your-mongodb-uri-here"
SECRET_KEY="your-random-secret-key"
```

### Step 3: Run the App

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## 🚀 Deployment on Vercel

1. Push your code to GitHub.
2. Go to [vercel.com](https://vercel.com/) and import the project.
3. In your project settings, add `MONGO_URI` and `SECRET_KEY` environment variables.
4. Click **Deploy**.

That's it — Vercel will handle everything for you! 🎉

---

© 2025 ServeSmart | Built with ❤️ by students for students
