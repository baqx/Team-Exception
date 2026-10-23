import sqlite3
import os
import uuid
import hashlib
import json
import secrets
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
import httpx
from app.config import settings

logger = logging.getLogger("user_service")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chalkka_data.db")

# ─── Supabase REST Client Helpers ─────────────────────────────────────────────

def _get_supabase_headers() -> Optional[Dict[str, str]]:
    key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_SECRET_KEY or settings.SUPABASE_ANON_KEY
    if not settings.SUPABASE_URL or not key:
        return None
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

def _supabase_request(
    method: str, 
    endpoint: str, 
    json_data: Any = None, 
    params: Optional[Dict[str, str]] = None
) -> Optional[Any]:
    """
    Executes a PostgREST query against the Supabase database.
    Returns:
      - Parsed JSON response (list or dict) on success
      - None if table not found (404), network error, or Supabase unconfigured
    """
    headers = _get_supabase_headers()
    if not headers or not settings.SUPABASE_URL:
        return None
        
    url = f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1/{endpoint}"
    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.request(method, url, headers=headers, json=json_data, params=params)
            if resp.status_code in (200, 201, 204):
                if resp.status_code == 204 or not resp.text.strip():
                    return []
                return resp.json()
            elif resp.status_code == 404:
                # Table not found (schema migration not yet executed in Supabase SQL editor)
                logger.info(f"[Supabase] Table '{endpoint}' not found (404). Falling back to local SQLite.")
                return None
            else:
                logger.warning(f"[Supabase] {method} {endpoint} returned {resp.status_code}: {resp.text}")
                return None
    except Exception as e:
        logger.warning(f"[Supabase] Connection error: {e}. Falling back to SQLite.")
        return None

# ─── Local SQLite Connection & Setup ──────────────────────────────────────────

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

# Initialize local fallback DB on module import
init_db()

def _hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()

# ─── User Management ──────────────────────────────────────────────────────────

def create_user(email: str, password: str, name: str) -> Dict[str, Any]:
    email = email.strip().lower()
    name = name.strip()
    salt = secrets.token_hex(16)
    pwd_hash = _hash_password(password, salt)
    user_id = str(uuid.uuid4())
    initial_credits = 50

    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        # Check if email exists
        existing = _supabase_request("GET", "users", params={"email": f"eq.{email}", "select": "id"})
        if existing is not None:
            if len(existing) > 0:
                raise ValueError("An account with this email already exists.")
            # Insert into Supabase
            inserted = _supabase_request("POST", "users", json_data={
                "id": user_id,
                "email": email,
                "password_hash": pwd_hash,
                "salt": salt,
                "name": name,
                "credits": initial_credits,
            })
            if inserted is not None:
                token = create_session(user_id)
                # Keep local SQLite in sync as cache
                _save_user_to_sqlite(user_id, email, pwd_hash, salt, name, initial_credits)
                return {
                    "id": user_id,
                    "email": email,
                    "name": name,
                    "credits": initial_credits,
                    "token": token
                }

    # 2. Local SQLite Fallback
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

def _save_user_to_sqlite(user_id: str, email: str, pwd_hash: str, salt: str, name: str, credits: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO users (id, email, password_hash, salt, name, credits) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, email, pwd_hash, salt, name, credits)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    email = email.strip().lower()

    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        users = _supabase_request("GET", "users", params={"email": f"eq.{email}", "select": "*"})
        if users is not None:
            if not users:
                return None
            user_data = users[0]
            computed_hash = _hash_password(password, user_data["salt"])
            if computed_hash != user_data["password_hash"]:
                return None
            token = create_session(user_data["id"])
            return {
                "id": user_data["id"],
                "email": user_data["email"],
                "name": user_data["name"],
                "credits": user_data.get("credits", 50),
                "token": token
            }

    # 2. Local SQLite Fallback
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

    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        inserted = _supabase_request("POST", "sessions", json_data={"token": token, "user_id": user_id})
        if inserted is not None:
            _save_session_to_sqlite(token, user_id)
            return token

    # 2. Local SQLite Fallback
    _save_session_to_sqlite(token, user_id)
    return token

def _save_session_to_sqlite(token: str, user_id: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_user_by_token(token: str) -> Optional[Dict[str, Any]]:
    if not token:
        return None

    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        sessions = _supabase_request("GET", "sessions", params={"token": f"eq.{token}", "select": "user_id"})
        if sessions is not None:
            if not sessions:
                return None
            user_id = sessions[0]["user_id"]
            return get_user_by_id(user_id)

    # 2. Local SQLite Fallback
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

    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        users = _supabase_request("GET", "users", params={"id": f"eq.{user_id}", "select": "id,email,name,credits,created_at"})
        if users is not None:
            if users:
                return users[0]
            return None

    # 2. Local SQLite Fallback
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
        return True

    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        user_data = get_user_by_id(user_id)
        if user_data is not None:
            current_credits = user_data.get("credits", 0)
            if current_credits < cost:
                return False
            new_credits = current_credits - cost
            _supabase_request("PATCH", "users", json_data={"credits": new_credits}, params={"id": f"eq.{user_id}"})
            # Also sync to local SQLite
            _update_sqlite_credits(user_id, new_credits)
            return True

    # 2. Local SQLite Fallback
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
    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        user_data = get_user_by_id(user_id)
        if user_data is not None:
            new_credits = user_data.get("credits", 0) + amount
            _supabase_request("PATCH", "users", json_data={"credits": new_credits}, params={"id": f"eq.{user_id}"})
            _update_sqlite_credits(user_id, new_credits)
            return new_credits

    # 2. Local SQLite Fallback
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET credits = credits + ? WHERE id = ?", (amount, user_id))
    cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return row["credits"] if row else 0

def _update_sqlite_credits(user_id: str, new_credits: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET credits = ? WHERE id = ?", (new_credits, user_id))
        conn.commit()
        conn.close()
    except Exception:
        pass

# ─── Job History Management ───────────────────────────────────────────────────

def record_job_start(job_id: str, user_id: Optional[str], query: str, subject: str, length: str):
    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        _supabase_request("POST", "user_jobs", json_data={
            "job_id": job_id,
            "user_id": user_id,
            "query": query,
            "subject": subject,
            "length": length,
            "status": "pending",
        })

    # 2. Also keep local SQLite updated
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO user_jobs (job_id, user_id, query, subject, length, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP)
        """, (job_id, user_id, query, subject, length))
        conn.commit()
        conn.close()
    except Exception:
        pass

def record_job_completion(job_id: str, video_url: str, lesson_plan_dict: Optional[Dict[str, Any]] = None):
    plan_json = json.dumps(lesson_plan_dict) if lesson_plan_dict else None
    now_iso = datetime.utcnow().isoformat()

    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        _supabase_request("PATCH", "user_jobs", json_data={
            "status": "completed",
            "video_url": video_url,
            "lesson_plan_json": plan_json,
            "completed_at": now_iso,
        }, params={"job_id": f"eq.{job_id}"})

    # 2. Local SQLite
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_jobs 
            SET status = 'completed', video_url = ?, lesson_plan_json = ?, completed_at = CURRENT_TIMESTAMP
            WHERE job_id = ?
        """, (video_url, plan_json, job_id))
        conn.commit()
        conn.close()
    except Exception:
        pass

def record_job_failure(job_id: str, error_message: Optional[str] = None):
    now_iso = datetime.utcnow().isoformat()

    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        _supabase_request("PATCH", "user_jobs", json_data={
            "status": "failed",
            "completed_at": now_iso,
        }, params={"job_id": f"eq.{job_id}"})

    # 2. Local SQLite
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_jobs 
            SET status = 'failed', completed_at = CURRENT_TIMESTAMP
            WHERE job_id = ?
        """, (job_id,))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_user_jobs(user_id: str) -> List[Dict[str, Any]]:
    # 1. Try Supabase
    headers = _get_supabase_headers()
    if headers:
        jobs = _supabase_request("GET", "user_jobs", params={
            "user_id": f"eq.{user_id}",
            "order": "created_at.desc",
            "select": "*"
        })
        if jobs is not None:
            results = []
            for d in jobs:
                if d.get("lesson_plan_json"):
                    try:
                        d["lesson_plan"] = json.loads(d["lesson_plan_json"]) if isinstance(d["lesson_plan_json"], str) else d["lesson_plan_json"]
                    except Exception:
                        d["lesson_plan"] = None
                else:
                    d["lesson_plan"] = None
                results.append(d)
            return results

    # 2. Local SQLite Fallback
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
