from flask import Flask, render_template, request, jsonify
import secrets
import string
import sqlite3

app = Flask(__name__)

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("passwords.db")

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

    # Enforce at least one from each selected set
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

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"

# ---------- ROUTES ----------
@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    strength = ""
    history = []

    if request.method == "POST":
        length = int(request.form.get("length", 12))

        password = generate_password(
            length,
            "upper" in request.form,
            "lower" in request.form,
            "digits" in request.form,
            "symbols" in request.form,
            "exclude" in request.form
        )

        if password:
            strength = password_strength(password)

            with get_db() as conn:
                conn.execute(
                    "INSERT INTO passwords (password) VALUES (?)",
                    (password,)
                )

                # Keep only last 5 passwords
                conn.execute("""
                    DELETE FROM passwords
                    WHERE id NOT IN (
                        SELECT id FROM passwords ORDER BY id DESC LIMIT 5
                    )
                """)

    with get_db() as conn:
        history = conn.execute(
            "SELECT password FROM passwords ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "index.html",
        password=password,
        strength=strength,
        history=history
    )

# ---------- OPTIONAL API ----------
@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.json

    pwd = generate_password(
        data["length"],
        data["uppercase"],
        data["lowercase"],
        data["digits"],
        data["symbols"],
        data.get("excludeSimilar", False)
    )

    return jsonify({
        "password": pwd,
        "strength": password_strength(pwd)
    })

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
