# ============================================
# StudyMate AI - Database Operations
# Uses SQLite (built into Python, no install)
# ============================================

import sqlite3
import hashlib
import os
from datetime import datetime


# ============================================
# DATABASE SETUP
# ============================================

DB_FILE = "studymate.db"


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def initialize_database():
    """Create all tables if they don't exist"""
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name   TEXT NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            program     TEXT,
            institution TEXT,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # MCQ History table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mcq_history (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            exam_mode     TEXT,
            program       TEXT,
            year          TEXT,
            institution   TEXT,
            subject       TEXT,
            topic         TEXT,
            difficulty    TEXT,
            num_questions INTEGER,
            mcq_content   TEXT,
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Assessment Results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            subject       TEXT,
            topic         TEXT,
            total_qs      INTEGER,
            correct       INTEGER,
            score_pct     REAL,
            difficulty    TEXT,
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Suggestions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suggestions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name  TEXT,
            category   TEXT,
            message    TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ============================================
# PASSWORD HASHING
# ============================================

def hash_password(password):
    """Convert password to secure hash"""
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================
# USER OPERATIONS
# ============================================

def create_user(full_name, email, password, program="", institution=""):
    """Register a new user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (full_name, email, password, program, institution)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, email, hash_password(password), program, institution))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, None, "Email already registered. Please login."
    except Exception as e:
        return False, None, f"Error: {str(e)}"


def login_user(email, password):
    """Verify login credentials"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE email = ? AND password = ?
        """, (email, hash_password(password)))
        user = cursor.fetchone()
        conn.close()
        if user:
            return True, dict(user), "Login successful!"
        return False, None, "Invalid email or password."
    except Exception as e:
        return False, None, f"Error: {str(e)}"


def get_user_by_id(user_id):
    """Get user details by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


# ============================================
# MCQ HISTORY OPERATIONS
# ============================================

def save_mcq_history(user_id, exam_mode, program, year,
                     institution, subject, topic,
                     difficulty, num_questions, mcq_content):
    """Save generated MCQ session to history"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mcq_history
            (user_id, exam_mode, program, year, institution,
             subject, topic, difficulty, num_questions, mcq_content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, exam_mode, program, year, institution,
              subject, topic, difficulty, num_questions, mcq_content))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def get_user_history(user_id, limit=20):
    """Get MCQ history for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM mcq_history
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_history_by_id(history_id, user_id):
    """Get a specific history record"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM mcq_history
        WHERE id = ? AND user_id = ?
    """, (history_id, user_id))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# ============================================
# ASSESSMENT OPERATIONS
# ============================================

def save_assessment(user_id, subject, topic,
                    total_qs, correct, difficulty):
    """Save assessment result"""
    score_pct = round((correct / total_qs) * 100, 1) if total_qs > 0 else 0
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO assessments
            (user_id, subject, topic, total_qs,
             correct, score_pct, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, subject, topic, total_qs,
              correct, score_pct, difficulty))
        conn.commit()
        conn.close()
        return True, score_pct
    except Exception as e:
        return False, 0


def get_user_assessments(user_id, limit=20):
    """Get assessment history for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM assessments
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_user_stats(user_id):
    """Get overall stats for dashboard"""
    conn = get_connection()
    cursor = conn.cursor()

    # Total MCQ sessions
    cursor.execute("""
        SELECT COUNT(*) as total FROM mcq_history WHERE user_id = ?
    """, (user_id,))
    total_sessions = cursor.fetchone()["total"]

    # Total MCQs generated
    cursor.execute("""
        SELECT SUM(num_questions) as total
        FROM mcq_history WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()
    total_mcqs = result["total"] if result["total"] else 0

    # Total assessments
    cursor.execute("""
        SELECT COUNT(*) as total FROM assessments WHERE user_id = ?
    """, (user_id,))
    total_assessments = cursor.fetchone()["total"]

    # Average score
    cursor.execute("""
        SELECT AVG(score_pct) as avg FROM assessments WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()
    avg_score = round(result["avg"], 1) if result["avg"] else 0

    # Best subject
    cursor.execute("""
        SELECT subject, AVG(score_pct) as avg
        FROM assessments WHERE user_id = ?
        GROUP BY subject ORDER BY avg DESC LIMIT 1
    """, (user_id,))
    best = cursor.fetchone()
    best_subject = best["subject"] if best else "N/A"

    conn.close()
    return {
        "total_sessions": total_sessions,
        "total_mcqs": total_mcqs,
        "total_assessments": total_assessments,
        "avg_score": avg_score,
        "best_subject": best_subject
    }
def save_suggestion(user_name, category, message):
    """Save user suggestion"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO suggestions (user_name, category, message)
            VALUES (?, ?, ?)
        """, (user_name, category, message))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def get_app_stats():
    """Get overall app usage stats"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM users")
    total_users = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM mcq_history")
    total_sessions = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(num_questions) as total FROM mcq_history")
    result = cursor.fetchone()
    total_mcqs = result["total"] if result["total"] else 0

    cursor.execute("SELECT COUNT(*) as total FROM assessments")
    total_tests = cursor.fetchone()["total"]

    conn.close()
    return {
        "total_users": total_users,
        "total_sessions": total_sessions,
        "total_mcqs": total_mcqs,
        "total_tests": total_tests
    }