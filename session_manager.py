# ============================================
# StudyMate AI - Session Manager
# Persistent login across browser refreshes
# ============================================

import sqlite3
import secrets
from datetime import datetime, timedelta

DB_FILE = "studymate.db"


def get_conn():
    conn = sqlite3.connect(
        DB_FILE, timeout=30,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def init_sessions_table():
    """Create sessions table if not exists"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            token      TEXT UNIQUE NOT NULL,
            expires_at TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def create_session(user_id):
    """Create 30-day session token"""
    token      = secrets.token_urlsafe(32)
    expires_at = (
        datetime.now() + timedelta(days=30)
    ).strftime("%Y-%m-%d %H:%M:%S")

    conn = get_conn()
    cursor = conn.cursor()
    # Remove old sessions for this user
    cursor.execute(
        "DELETE FROM user_sessions WHERE user_id = ?",
        (user_id,)
    )
    cursor.execute("""
        INSERT INTO user_sessions
        (user_id, token, expires_at)
        VALUES (?, ?, ?)
    """, (user_id, token, expires_at))
    conn.commit()
    conn.close()
    return token


def validate_session(token):
    """Check if token is valid, return user dict"""
    if not token or len(token) < 10:
        return None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            SELECT u.id, u.full_name, u.email,
                   u.program, u.institution,
                   u.created_at
            FROM user_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ?
            AND s.expires_at > ?
        """, (token, now))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception as e:
        print(f"validate_session error: {e}")
        return None


def delete_session(token):
    """Delete session on logout"""
    if not token:
        return
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM user_sessions WHERE token = ?",
            (token,)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"delete_session error: {e}")