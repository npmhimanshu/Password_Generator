from flask import Flask, render_template, request, jsonify
import secrets
import string
import sqlite3
import math
import requests

app = Flask(__name__)
DB_NAME = "passwords.db"

# 🔑 OpenRouter Config
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"
OPENROUTER_MODEL = "openai/gpt-3.5-turbo"

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT NOT NULL
            )
        """)

init_db()

# ---------- PASSWORD LOGIC ----------
def generate_password(length, exclude_similar=False):
    if length < 4:
        raise ValueError("Password length must be at least 4")

    U = string.ascii_uppercase
    L = string.ascii_lowercase
    D = string.digits
    S = string.punctuation

    if exclude_similar:
        for c in "O0l1I":
            U = U.replace(c, "")
            L = L.replace(c, "")
            D = D.replace(c, "")

    password = [
        secrets.choice(U),
        secrets.choice(L),
        secrets.choice(D),
        secrets.choice(S)
    ]

    all_chars = U + L + D + S

    while len(password) < length:
        password.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password)
    return "".join(password)

def password_strength(pwd):
    score = 0
    if len(pwd) >= 8: score += 1
    if len(pwd) >= 12: score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.islower() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(not c.isalnum() for c in pwd): score += 1

    if score <= 2: return "Weak"
    elif score <= 4: return "Medium"
    return "Strong"

def password_entropy(pwd, exclude_similar):
    pool = 0
    pool += len(string.ascii_uppercase.replace("O", "").replace("I", "")) if exclude_similar else len(string.ascii_uppercase)
    pool += len(string.ascii_lowercase.replace("l", "")) if exclude_similar else len(string.ascii_lowercase)
    pool += len(string.digits.replace("0", "").replace("1", "")) if excl
