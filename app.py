from flask import Flask, render_template, request
import random
import string
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    chars = ""
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation

    if chars == "":
        return ""

    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    history = []

    if request.method == "POST":
        length = int(request.form.get("length"))
        password = generate_password(
            length,
            "upper" in request.form,
            "lower" in request.form,
            "digits" in request.form,
            "symbols" in request.form
        )

        if password:
            conn = sqlite3.connect("passwords.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO passwords (password) VALUES (?)", (password,))
            conn.commit()

            # Keep only last 5 passwords
            cur.execute("""
                DELETE FROM passwords
                WHERE id NOT IN (
                    SELECT id FROM passwords ORDER BY id DESC LIMIT 5
                )
            """)
            conn.commit()
            conn.close()

    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()
    cur.execute("SELECT password FROM passwords ORDER BY id DESC")
    history = cur.fetchall()
    conn.close()

    return render_template("index.html", password=password, history=history)

if __name__ == "__main__":
    app.run(debug=True)
