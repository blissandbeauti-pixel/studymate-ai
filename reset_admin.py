import sqlite3
import hashlib

DB_FILE  = "studymate.db"
NEW_PASS = "Wru@studymate4me"
hashed   = hashlib.sha256(NEW_PASS.encode()).hexdigest()

conn   = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Check which tables exist
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)
tables = [r[0] for r in cursor.fetchall()]
print("Tables found:", tables)

# Reset in admins_v2
if "admins_v2" in tables:
    cursor.execute("""
        UPDATE admins_v2
        SET password = ?
        WHERE username = 'admin'
    """, (hashed,))
    print(f"admins_v2 rows updated: {cursor.rowcount}")

# Reset in admins (old table)
if "admins" in tables:
    cursor.execute("""
        UPDATE admins
        SET password = ?
        WHERE username = 'admin'
    """, (hashed,))
    print(f"admins rows updated: {cursor.rowcount}")

# If no rows updated — insert fresh admin
cursor.execute(
    "SELECT COUNT(*) as c FROM admins_v2 WHERE username='admin'"
) if "admins_v2" in tables else None

conn.commit()
conn.close()
print(f"✅ Done. Password set to: {NEW_PASS}")