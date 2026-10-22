import sqlite3
import os
import uuid
import hashlib
import json
import secrets
from datetime import datetime
from typing import Optional, List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chalkka_data.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            name TEXT NOT NULL,
            credits INTEGER NOT NULL DEFAULT 50,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User Jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_jobs (
            job_id TEXT PRIMARY KEY,
            user_id TEXT,
            query TEXT NOT NULL,
            subject TEXT,
            length TEXT,
            status TEXT DEFAULT 'pending',
            video_url TEXT,
            lesson_plan_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize DB on module import
init_db()

def _hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()

def create_user(email: str, password: str, name: str) -> Dict[str, Any]:
    email = email.strip().lower()
    name = name.strip()
    salt = secrets.token_hex(16)
    pwd_hash = _hash_password(password, salt)
    user_id = str(uuid.uuid4())
    initial_credits = 50

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (id, email, password_hash, salt, name, credits) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, email, pwd_hash, salt, name, initial_credits)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError("An account with this email already exists.")
    
    token = create_session(user_id)
    conn.close()
    return {
        "id": user_id,
        "email": email,
        "name": name,
        "credits": initial_credits,
        "token": token
    }

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    email = email.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, password_hash, salt, name, credits FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    computed_hash = _hash_password(password, row["salt"])
    if computed_hash != row["password_hash"]:
        return None
        
    token = create_session(row["id"])
    return {
        "id": row["id"],
        "email": row["email"],
        "name": row["name"],
        "credits": row["credits"],
        "token": token
    }

def create_session(user_id: str) -> str:
    token = secrets.token_hex(32)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id))
    conn.commit()
    conn.close()
    return token

def get_user_by_token(token: str) -> Optional[Dict[str, Any]]:
    if not token:
        return None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.email, u.name, u.credits, u.created_at
        FROM users u
        JOIN sessions s ON u.id = s.user_id
        WHERE s.token = ?
    """, (token,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    if not user_id:
        return None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, name, credits, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def check_and_deduct_credits(user_id: str, cost: int = 5) -> bool:
    """
    Atomically checks if the user has at least `cost` credits, and deducts them.
    Returns True if deduction succeeded, False if insufficient credits.
    """
    if not user_id:
        return True # Guest user bypass or handled separately
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row or row["credits"] < cost:
        conn.close()
        return False
    
    cursor.execute("UPDATE users SET credits = credits - ? WHERE id = ?", (cost, user_id))
    conn.commit()
    conn.close()
    return True

def add_credits(user_id: str, amount: int = 25) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET credits = credits + ? WHERE id = ?", (amount, user_id))
    cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return row["credits"] if row else 0

def record_job_start(job_id: str, user_id: Optional[str], query: str, subject: str, length: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO user_jobs (job_id, user_id, query, subject, length, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP)
    """, (job_id, user_id, query, subject, length))
    conn.commit()
    conn.close()

def record_job_completion(job_id: str, video_url: str, lesson_plan_dict: Optional[Dict[str, Any]] = None):
    conn = get_connection()
    cursor = conn.cursor()
    plan_json = json.dumps(lesson_plan_dict) if lesson_plan_dict else None
    cursor.execute("""
        UPDATE user_jobs 
        SET status = 'completed', video_url = ?, lesson_plan_json = ?, completed_at = CURRENT_TIMESTAMP
        WHERE job_id = ?
    """, (video_url, plan_json, job_id))
    conn.commit()
    conn.close()

def record_job_failure(job_id: str, error_message: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_jobs 
        SET status = 'failed', completed_at = CURRENT_TIMESTAMP
        WHERE job_id = ?
    """, (job_id,))
    conn.commit()
    conn.close()

def get_user_jobs(user_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT job_id, user_id, query, subject, length, status, video_url, lesson_plan_json, created_at, completed_at
        FROM user_jobs
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        if d.get("lesson_plan_json"):
            try:
                d["lesson_plan"] = json.loads(d["lesson_plan_json"])
            except Exception:
                d["lesson_plan"] = None
        else:
            d["lesson_plan"] = None
        results.append(d)
    return results
