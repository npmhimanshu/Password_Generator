from flask import Flask, render_template, request, jsonify
import secrets
import string
import sqlite3
import math

app = Flask(__name__)
DB_NAME = "passwords.db"

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT
            )
        """)

init_db()

# ---------- PASSWORD LOGIC ----------
def generate_password(length, upper, lower, digits, symbols, exclude_similar):
    sets = []

    U = string.ascii_uppercase
    L = string.ascii_lowercase
    D = string.digits
    S = string.punctuation

    if exclude_similar:
        for c in "O0l1I":
            U = U.replace(c, "")
            L = L.replace(c, "")
            D = D.replace(c, "")

    if upper: sets.append(U)
    if lower: sets.append(L)
    if digits: sets.append(D)
    if symbols: sets.append(S)

    if not sets:
        return ""

    all_chars = "".join(sets)

    # Ensure at least one from each selected set
    password = [secrets.choice(s) for s in sets]

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

def password_entropy(pwd, upper, lower, digits, symbols):
    pool = 0
    if upper: pool += len(string.ascii_uppercase)
    if lower: pool += len(string.ascii_lowercase)
    if digits: pool += len(string.digits)
    if symbols: pool += len(string.punctuation)
    if pool == 0: return 0
    return round(math.log2(pool ** len(pwd)), 2)

# ---------- ROUTES ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_api():
    data = request.json

    password = generate_password(
        data.get("length", 12),
        data.get("upper", True),
        data.get("lower", True),
        data.get("digits", True),
        data.get("symbols", False),
        data.get("excludeSimilar", False)
    )

    strength = password_strength(password)
    entropy = password_entropy(
        password,
        data.get("upper", True),
        data.get("lower", True),
        data.get("digits", True),
        data.get("symbols", False)
    )

    # Save and maintain history
    with get_db() as conn:
        conn.execute("INSERT INTO passwords (password) VALUES (?)", (password,))
        conn.execute("""
            DELETE FROM passwords
            WHERE id NOT IN (
                SELECT id FROM passwords ORDER BY id DESC LIMIT 5
            )
        """)
        history = conn.execute(
            "SELECT password FROM passwords ORDER BY id DESC LIMIT 5"
        ).fetchall()

    return jsonify({
        "password": password,
        "strength": strength,
        "entropy": entropy,
        "history": [h[0] for h in history]
    })

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
