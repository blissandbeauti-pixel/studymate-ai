<<<<<<< HEAD
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

    # Admin table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT UNIQUE NOT NULL,
            password   TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Exam countdowns table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_countdowns (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id   INTEGER NOT NULL,
            exam_name TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            subject   TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Past papers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS past_papers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            board       TEXT,
            program     TEXT,
            subject     TEXT,
            year        TEXT,
            paper_type  TEXT,
            file_path   TEXT,
            uploaded_by TEXT,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Roles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name   TEXT UNIQUE NOT NULL,
            can_manage_users    INTEGER DEFAULT 0,
            can_manage_papers   INTEGER DEFAULT 1,
            can_view_stats      INTEGER DEFAULT 1,
            can_manage_admins   INTEGER DEFAULT 0,
            can_manage_teachers INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Update admins table with role and master flag
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins_v2 (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            full_name   TEXT NOT NULL,
            email       TEXT,
            password    TEXT NOT NULL,
            is_master   INTEGER DEFAULT 0,
            role_id     INTEGER,
            is_active   INTEGER DEFAULT 1,
            created_by  INTEGER,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
    """)

    # Teacher profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teacher_profiles (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER UNIQUE NOT NULL,
            full_name       TEXT NOT NULL,
            qualification   TEXT,
            experience_yrs  INTEGER DEFAULT 0,
            master_subjects TEXT,
            city            TEXT,
            contact_info    TEXT,
            services        TEXT,
            hourly_rate     TEXT,
            availability    TEXT,
            bio             TEXT,
            photo_path      TEXT,
            is_verified     INTEGER DEFAULT 0,
            is_active       INTEGER DEFAULT 1,
            created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Terms acceptance log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS terms_acceptance (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            accepted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            ip_note     TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Password reset tokens
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            token       TEXT NOT NULL,
            expires_at  TEXT NOT NULL,
            used        INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Update users table — add account_type column safely
    try:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN account_type TEXT DEFAULT 'student'"
        )
    except Exception:
        pass  # Column already exists

    # Insert default roles
    cursor.execute("SELECT COUNT(*) as c FROM roles")
    if cursor.fetchone()["c"] == 0:
        default_roles = [
            ("Content Manager", 0, 1, 1, 0, 0),
            ("User Manager", 1, 0, 1, 0, 0),
            ("Analytics Viewer", 0, 0, 1, 0, 0),
            ("Teacher Verifier", 0, 0, 1, 0, 1),
        ]
        for role in default_roles:
            cursor.execute("""
                INSERT INTO roles
                (role_name, can_manage_users, can_manage_papers,
                 can_view_stats, can_manage_admins, can_manage_teachers)
                VALUES (?, ?, ?, ?, ?, ?)
            """, role)

    # Create master admin
    cursor.execute("SELECT COUNT(*) as c FROM admins_v2 WHERE is_master=1")
    if cursor.fetchone()["c"] == 0:
        master_pwd = hashlib.sha256(
            "Wru@studymate4me".encode()
        ).hexdigest()
        cursor.execute("""
            INSERT INTO admins_v2
            (username, full_name, email, password, is_master, is_active)
            VALUES (?, ?, ?, ?, 1, 1)
        """, ("admin", "Master Admin", "admin@studymate.ai", master_pwd))

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
# ============================================
# ADMIN OPERATIONS
# ============================================

def login_admin(username, password):
    """Verify admin credentials"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM admins
            WHERE username = ? AND password = ?
        """, (username, hash_password(password)))
        admin = cursor.fetchone()
        conn.close()
        if admin:
            return True, dict(admin), "Login successful!"
        return False, None, "Invalid credentials."
    except Exception as e:
        return False, None, f"Error: {str(e)}"


def get_all_users(limit=100):
    """Get all registered users"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.*,
            COUNT(DISTINCT m.id) as total_sessions,
            COUNT(DISTINCT a.id) as total_tests,
            COALESCE(AVG(a.score_pct), 0) as avg_score
        FROM users u
        LEFT JOIN mcq_history m ON u.id = m.user_id
        LEFT JOIN assessments a ON u.id = a.user_id
        GROUP BY u.id
        ORDER BY u.created_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_suggestions(limit=100):
    """Get all suggestions"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM suggestions
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_user(user_id):
    """Delete a user and their data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM mcq_history WHERE user_id = ?", (user_id,)
        )
        cursor.execute(
            "DELETE FROM assessments WHERE user_id = ?", (user_id,)
        )
        cursor.execute(
            "DELETE FROM exam_countdowns WHERE user_id = ?", (user_id,)
        )
        cursor.execute(
            "DELETE FROM users WHERE id = ?", (user_id,)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def get_full_stats():
    """Get complete app statistics"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as t FROM users")
    total_users = cursor.fetchone()["t"]

    cursor.execute("SELECT COUNT(*) as t FROM mcq_history")
    total_sessions = cursor.fetchone()["t"]

    cursor.execute(
        "SELECT COALESCE(SUM(num_questions),0) as t FROM mcq_history"
    )
    total_mcqs = cursor.fetchone()["t"]

    cursor.execute("SELECT COUNT(*) as t FROM assessments")
    total_tests = cursor.fetchone()["t"]

    cursor.execute("SELECT COUNT(*) as t FROM suggestions")
    total_suggestions = cursor.fetchone()["t"]

    cursor.execute(
        "SELECT COALESCE(AVG(score_pct),0) as t FROM assessments"
    )
    overall_avg = round(cursor.fetchone()["t"], 1)

    # Most popular subject
    cursor.execute("""
        SELECT subject, COUNT(*) as cnt
        FROM mcq_history GROUP BY subject
        ORDER BY cnt DESC LIMIT 1
    """)
    row = cursor.fetchone()
    top_subject = row["subject"] if row else "N/A"

    # Daily registrations (last 7 days)
    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as cnt
        FROM users
        WHERE created_at >= DATE('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    """)
    daily_users = [dict(r) for r in cursor.fetchall()]

    # Daily MCQ sessions (last 7 days)
    cursor.execute("""
        SELECT DATE(created_at) as date,
               COUNT(*) as cnt,
               SUM(num_questions) as mcqs
        FROM mcq_history
        WHERE created_at >= DATE('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    """)
    daily_sessions = [dict(r) for r in cursor.fetchall()]

    # Top programs
    cursor.execute("""
        SELECT program, COUNT(*) as cnt
        FROM mcq_history
        GROUP BY program
        ORDER BY cnt DESC LIMIT 5
    """)
    top_programs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        "total_users": total_users,
        "total_sessions": total_sessions,
        "total_mcqs": total_mcqs,
        "total_tests": total_tests,
        "total_suggestions": total_suggestions,
        "overall_avg": overall_avg,
        "top_subject": top_subject,
        "daily_users": daily_users,
        "daily_sessions": daily_sessions,
        "top_programs": top_programs
    }


# ============================================
# EXAM COUNTDOWN OPERATIONS
# ============================================

def save_exam_countdown(user_id, exam_name, exam_date, subject=""):
    """Save exam countdown for student"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO exam_countdowns
            (user_id, exam_name, exam_date, subject)
            VALUES (?, ?, ?, ?)
        """, (user_id, exam_name, exam_date, subject))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def get_user_countdowns(user_id):
    """Get all countdowns for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM exam_countdowns
        WHERE user_id = ?
        ORDER BY exam_date ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_countdown(countdown_id, user_id):
    """Delete a countdown"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM exam_countdowns
            WHERE id = ? AND user_id = ?
        """, (countdown_id, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


# ============================================
# PROGRESS ANALYTICS
# ============================================

def get_subject_progress(user_id):
    """Get subject-wise performance for charts"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            subject,
            COUNT(*) as attempts,
            AVG(score_pct) as avg_score,
            MAX(score_pct) as best_score,
            SUM(total_qs) as total_questions,
            SUM(correct) as total_correct
        FROM assessments
        WHERE user_id = ?
        GROUP BY subject
        ORDER BY avg_score DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_score_trend(user_id, limit=10):
    """Get score trend over time"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, topic, score_pct,
               difficulty, created_at
        FROM assessments
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ============================================
# PAST PAPERS
# ============================================

def save_past_paper(title, board, program,
                    subject, year, paper_type,
                    file_path, uploaded_by):
    """Save past paper record"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO past_papers
            (title, board, program, subject,
             year, paper_type, file_path, uploaded_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, board, program, subject,
              year, paper_type, file_path, uploaded_by))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def get_past_papers(board=None, program=None, subject=None):
    """Get past papers with optional filters"""
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM past_papers WHERE 1=1"
    params = []
    if board:
        query += " AND board = ?"
        params.append(board)
    if program:
        query += " AND program = ?"
        params.append(program)
    if subject:
        query += " AND subject LIKE ?"
        params.append(f"%{subject}%")
    query += " ORDER BY created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ============================================
# ADMIN V2 OPERATIONS
# ============================================

def login_admin_v2(username, password):
    """Login for master and sub-admins"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, r.role_name,
                r.can_manage_users, r.can_manage_papers,
                r.can_view_stats, r.can_manage_admins,
                r.can_manage_teachers
            FROM admins_v2 a
            LEFT JOIN roles r ON a.role_id = r.id
            WHERE a.username = ? AND a.password = ?
            AND a.is_active = 1
        """, (username, hash_password(password)))
        admin = cursor.fetchone()
        conn.close()
        if admin:
            return True, dict(admin), "Login successful!"
        return False, None, "Invalid credentials or account inactive."
    except Exception as e:
        return False, None, f"Error: {str(e)}"


def change_admin_password(admin_id, old_password, new_password):
    """Change admin password — only master admin can change others"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE admins_v2 SET password = ?
            WHERE id = ? AND password = ?
        """, (hash_password(new_password),
              admin_id, hash_password(old_password)))
        changed = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return changed
    except Exception:
        return False


def master_change_admin_password(admin_id, new_password):
    """Master admin changes any admin password without old password"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE admins_v2 SET password = ? WHERE id = ?
        """, (hash_password(new_password), admin_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def create_sub_admin(username, full_name, email,
                     password, role_id, created_by):
    """Master admin creates sub-admin"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO admins_v2
            (username, full_name, email, password,
             is_master, role_id, is_active, created_by)
            VALUES (?, ?, ?, ?, 0, ?, 1, ?)
        """, (username, full_name, email,
              hash_password(password), role_id, created_by))
        conn.commit()
        conn.close()
        return True, "Sub-admin created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    except Exception as e:
        return False, str(e)


def get_all_admins():
    """Get all admins with their roles"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, r.role_name
        FROM admins_v2 a
        LEFT JOIN roles r ON a.role_id = r.id
        ORDER BY a.is_master DESC, a.created_at ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_roles():
    """Get all available roles"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM roles ORDER BY role_name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def toggle_admin_status(admin_id):
    """Activate/deactivate sub-admin"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE admins_v2
            SET is_active = CASE WHEN is_active=1 THEN 0 ELSE 1 END
            WHERE id = ? AND is_master = 0
        """, (admin_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


# ============================================
# USER ACCOUNT OPERATIONS
# ============================================

def change_user_password(user_id, old_password, new_password):
    """User changes own password"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET password = ?
            WHERE id = ? AND password = ?
        """, (hash_password(new_password),
              user_id, hash_password(old_password)))
        changed = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return changed, (
            "Password changed successfully!"
            if changed else "Current password is incorrect."
        )
    except Exception as e:
        return False, str(e)


def save_terms_acceptance(user_id):
    """Log user's acceptance of terms"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO terms_acceptance (user_id)
            VALUES (?)
        """, (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def create_password_reset_token(email):
    """Create reset token for forgot password"""
    import secrets
    from datetime import datetime, timedelta
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Find user by email
        cursor.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        )
        user = cursor.fetchone()
        if not user:
            conn.close()
            return False, None, "No account found with this email."

        # Generate secure token
        token = secrets.token_urlsafe(32)
        expires = (
            datetime.now() + timedelta(hours=1)
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Save token
        cursor.execute("""
            INSERT INTO password_resets (user_id, token, expires_at)
            VALUES (?, ?, ?)
        """, (user["id"], token, expires))
        conn.commit()
        conn.close()
        return True, token, "Reset token created."
    except Exception as e:
        return False, None, str(e)


def reset_password_with_token(token, new_password):
    """Reset password using valid token"""
    from datetime import datetime
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM password_resets
            WHERE token = ? AND used = 0
            AND expires_at > ?
        """, (token, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        reset = cursor.fetchone()
        if not reset:
            conn.close()
            return False, "Token invalid or expired."

        cursor.execute("""
            UPDATE users SET password = ? WHERE id = ?
        """, (hash_password(new_password), reset["user_id"]))
        cursor.execute("""
            UPDATE password_resets SET used = 1 WHERE id = ?
        """, (reset["id"],))
        conn.commit()
        conn.close()
        return True, "Password reset successfully!"
    except Exception as e:
        return False, str(e)


# ============================================
# TEACHER PROFILES
# ============================================

def save_teacher_profile(user_id, data):
    """Save or update teacher profile"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO teacher_profiles
            (user_id, full_name, qualification, experience_yrs,
             master_subjects, city, contact_info, services,
             hourly_rate, availability, bio, photo_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, data["full_name"], data["qualification"],
            data["experience_yrs"], data["master_subjects"],
            data["city"], data["contact_info"], data["services"],
            data["hourly_rate"], data["availability"],
            data["bio"], data.get("photo_path", "")
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def get_teacher_profile(user_id):
    """Get teacher profile by user ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM teacher_profiles WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_teachers(subject_filter=None, city_filter=None):
    """Get all active verified teacher profiles"""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT t.*, u.email
        FROM teacher_profiles t
        JOIN users u ON t.user_id = u.id
        WHERE t.is_active = 1
    """
    params = []
    if subject_filter:
        query += " AND t.master_subjects LIKE ?"
        params.append(f"%{subject_filter}%")
    if city_filter:
        query += " AND t.city LIKE ?"
        params.append(f"%{city_filter}%")
    query += " ORDER BY t.is_verified DESC, t.created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def verify_teacher(teacher_id, status):
    """Admin verifies/unverifies a teacher"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE teacher_profiles
            SET is_verified = ? WHERE id = ?
        """, (status, teacher_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
=======
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
>>>>>>> b09323630fd2f2924f4f0231828396c7cbd43d21
