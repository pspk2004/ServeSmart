# ServeSmart - A Modern College Mess Management System

ServeSmart is a comprehensive, full-stack web application designed to solve the logistical challenges of traditional college and hostel mess systems. It replaces inefficient, paper-based processes with a streamlined, reliable, and user-friendly digital platform.

### The Problem
Traditional college mess systems are often plagued by inefficiencies:
- **Manual Bookkeeping:** Reliance on paper registers for tracking meals leads to accounting errors and significant administrative overhead.
- **Chaotic Queues:** The process of issuing and verifying meal tokens manually can cause long, frustrating queues for students.
- **Lack of Transparency:** Students have no easy way to track their spending, view their meal history, or know their current point balance.
- **Wastage:** Without accurate data on daily meal registrations, administrators cannot effectively predict demand, leading to food wastage.

### The Solution: ServeSmart
ServeSmart digitizes and streamlines this entire workflow, creating a seamless and transparent experience for both students and mess administrators. It is an end-to-end digital solution that handles everything from a student registering for a meal on their phone to an admin verifying it instantly with a QR code scanner.

This project bridges the gap between students and mess management, providing a single source of truth for all meal-related activities. It is a production-ready solution designed for reliability, ease of use, and deployment on modern cloud infrastructure.

## 🚀 Live Demo

**You can access the live, deployed application here:**

### **[https://serve-smart-teal.vercel.app/](https://serve-smart-teal.vercel.app/)**

---

## 🔑 Login Credentials

You can use the following sample credentials to test the application:

### 🧑‍💼 Admin Account
- **Roll Number:** `admin`
- **Password:** `adminpass`

### 🎓 Student Account
- **Roll Number:** `2022bcs0095`
- **Password:** `pspk`

You can also register your own new student accounts.

---

## ✨ Core Features

### For Students
- **Simple Registration & Login:** Secure authentication using unique college roll numbers.
- **Point-Based System:** Students start with a point balance that is used for meal registrations.
- **Instant QR Code Generation:** Upon successful meal registration, a unique QR code token is instantly generated and displayed in a pop-up modal without reloading the page.
- **Active Token Display:** An "Active Tokens" section on the dashboard prominently displays all unused QR codes for the current day, ensuring a student can never lose their token.
- **Meal & Point History:** Track a complete history of all registered meals and their status (Used/Not Used).

### For Administrators
- **Secure Admin Login:** A separate, secure login for mess administrators.
- **Three-Tier Verification System:** A robust and flexible system for verifying meal tokens:
    1.  **Live QR Code Scanner:** The primary method is a real-time, camera-based QR code scanner for instant and error-free token verification.
    2.  **Manual Token Entry:** A backup option to manually type in a token ID if the scanner fails or is unavailable.
    3.  **One-Click List Verification:** A third backup allowing the admin to find a student in the daily registration list and verify their meal with a single click.
- **Daily Registration Overview:** A dashboard that lists all students who have registered for meals on the current day, their token ID, and its current status (Verified/Not Verified).

---

## 🛠️ Tech Stack

- **Backend:** **Python** with the **Flask** web framework.
- **Database:** **PostgreSQL** (hosted on **Vercel Postgres**).
- **ORM:** **Flask-SQLAlchemy** for elegant and robust database interaction.
- **Frontend:** **HTML5**, **CSS3**, and **JavaScript** with the **Bootstrap 5** framework for a clean, responsive UI.
- **Deployment:** The application is hosted on **Vercel**.
- **Static File Serving:** **WhiteNoise** for robust production file serving.
- **QR Code Generation:** `qrcode` Python library.
- **QR Code Scanning:** `html5-qrcode` JavaScript library for live camera scanning.

---

## ⚙️ How to Run Locally

Follow these steps to get a copy of the project up and running on your own computer for development and testing.

### Prerequisites

- Python 3.9+
- A code editor like Visual Studio Code.
- A free Vercel account (to host the Postgres database).

### 1. Set Up the Database on Vercel

This project is designed to connect to a Vercel Postgres database, which is free and easy to set up.

1.  **Create a Vercel Postgres Database:** Log in to your Vercel account, go to the "Storage" tab, and create a new, free Postgres database.
2.  **Get Your Connection String:** In the database settings, go to the ".env.local" or "Connection Strings" tab and copy the `POSTGRES_URL`. This is your complete database address and password.

### 2. Set Up the Project Locally

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/pspk2004/ServeSmart.git
    cd ServeSmart
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # For Windows
    py -m venv venv
    venv\Scripts\activate

    # For macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create Your `.env` File:** Create a file named `.env` in the root folder and add your secret keys. **This file should not be committed to Git.**
    ```
    # Paste the database URL you copied from Vercel.
    # Make sure it starts with "postgresql://"
    POSTGRES_URL="postgresql://default:YourPassword...@..."

    # Create a long, random string for security
    SECRET_KEY="a-very-long-and-random-secret-key-for-local-dev"
    ```

5.  **Run the Application:** The application is self-initializing. The first time it runs, it will create all the necessary tables and seed the data.
    ```bash
    python app.py
    ```
    Open your browser and go to `http://127.0.0.1:5000`.