# app.py
# This single file contains the entire backend for the MCQ Exam Platform.

import os
import psycopg2
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ---------------------------------
# 1. INITIALIZE AND CONFIGURE THE APP
# ---------------------------------
load_dotenv() # Load environment variables from a .env file for local development

app = Flask(__name__)
CORS(app) # Enable CORS to allow frontend communication

# Secret key for signing JWTs. In production, use a strong, random key.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-default-secret-key')

# ---------------------------------
# 2. DATABASE CONNECTION
# ---------------------------------
# Get the database URL from environment variables (Railway will provide this)
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# ---------------------------------
# 3. DATABASE SETUP (TABLE CREATION)
# ---------------------------------
def setup_database():
    """Creates all necessary tables if they don't already exist."""
    conn = get_db_connection()
    if conn is None:
        print("Could not connect to the database. Aborting setup.")
        return

    cur = conn.cursor()

    # SQL commands to create tables
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(11) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            school VARCHAR(100),
            points INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS question_sets (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(50) NOT NULL, -- 'daily', 'weekly', 'monthly', 'subject'
            is_active BOOLEAN DEFAULT FALSE,
            exam_time_minutes INTEGER DEFAULT 30,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            set_id INTEGER REFERENCES question_sets(id) ON DELETE CASCADE,
            question_text TEXT NOT NULL,
            options JSONB NOT NULL, -- e.g., {"options": ["A", "B", "C", "D"]}
            correct_option VARCHAR(255) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS results (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            set_id INTEGER REFERENCES question_sets(id) ON DELETE CASCADE,
            score INTEGER NOT NULL,
            total_marks INTEGER NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    try:
        for command in commands:
            cur.execute(command)
        print("Tables created or already exist.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error during table creation: {error}")
    finally:
        cur.close()
        conn.commit()
        conn.close()

# Run this function once when the app starts to ensure tables are ready
setup_database()


# ---------------------------------
# 4. API ENDPOINTS
# ---------------------------------

# A simple test route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Python MCQ Exam API!"})

# --- USER AUTHENTICATION ---
@app.route('/api/signup', methods=['POST'])
def signup():
    # TODO: Get name, phone, password, school from request.json
    # TODO: Validate phone number format
    # TODO: Hash the password using bcrypt
    # TODO: Insert new user into the 'users' table
    # TODO: Return success message or error
    return jsonify({"message": "Signup endpoint not implemented yet."}), 501

@app.route('/api/login', methods=['POST'])
def login():
    # TODO: Get phone, password from request.json
    # TODO: Find user by phone in the 'users' table
    # TODO: Check if user exists and password is correct using bcrypt.checkpw
    # TODO: If valid, create a JWT token
    # TODO: Return the token and user info
    return jsonify({"message": "Login endpoint not implemented yet."}), 501

# --- EXAM ROUTES (for students) ---
@app.route('/api/exams/live', methods=['GET'])
def get_live_exam():
    # TODO: Find the question_set where is_active is TRUE
    # TODO: Get all questions for that set_id
    # TODO: Implement shuffle logic for questions and options if enabled
    # TODO: Implement "hard mode" logic (select random 30 questions)
    # TODO: Return the list of questions and exam time
    return jsonify({"message": "Get live exam endpoint not implemented yet."}), 501

@app.route('/api/exams/submit', methods=['POST'])
def submit_exam():
    # TODO: Get user_id (from JWT token), set_id, and answers from request.json
    # TODO: Calculate the score by comparing answers with correct_option in the 'questions' table
    # TODO: Save the result (user_id, set_id, score, total_marks) into the 'results' table
    # TODO: Update the user's points and level in the 'users' table
    # TODO: Return the final score and correct answers
    return jsonify({"message": "Submit exam endpoint not implemented yet."}), 501


# --- ADMIN PANEL ROUTES ---
@app.route('/api/admin/question-sets', methods=['POST', 'GET'])
def manage_question_sets():
    if request.method == 'POST':
        # TODO: Create a new question set
        return jsonify({"message": "Create question set not implemented."}), 501
    if request.method == 'GET':
        # TODO: Get all existing question sets
        return jsonify({"message": "Get all question sets not implemented."}), 501

@app.route('/api/admin/question-sets/<int:set_id>', methods=['DELETE', 'PUT'])
def manage_single_question_set(set_id):
    if request.method == 'DELETE':
        # TODO: Delete a question set and all its questions
        return jsonify({"message": f"Delete set {set_id} not implemented."}), 501
    if request.method == 'PUT':
        # TODO: Update a question set (e.g., set it to active)
        return jsonify({"message": f"Update set {set_id} not implemented."}), 501

@app.route('/api/admin/questions', methods=['POST'])
def add_question():
    # TODO: Get set_id, question_text, options, correct_option from request.json
    # TODO: Insert the new question into the 'questions' table
    return jsonify({"message": "Add question endpoint not implemented."}), 501

@app.route('/api/admin/results', methods=['GET'])
def get_all_results():
    # TODO: Get all results from the 'results' table, joining with user and set info
    # TODO: Allow filtering by set_id
    return jsonify({"message": "Get all results endpoint not implemented."}), 501


# --- LEADERBOARD & RESULTS ROUTES ---
@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    # TODO: Get query parameter for time frame (today, weekly, all-time)
    # TODO: Query the 'results' or 'users' table accordingly
    # TODO: Return top performers based on score or points
    return jsonify({"message": "Leaderboard endpoint not implemented."}), 501

@app.route('/api/my-results', methods=['GET'])
def get_my_results():
    # TODO: Get user_id from JWT token
    # TODO: Query the 'results' table for that user_id
    # TODO: Return all past results for the user
    return jsonify({"message": "My results endpoint not implemented."}), 501


# ---------------------------------
# 5. RUN THE APPLICATION
# ---------------------------------
if __name__ == '__main__':
    # The host='0.0.0.0' makes the server publicly available
    # This is necessary for platforms like Railway.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
