from flask import Flask, render_template, request
import random
import string
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history (password TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    chars = ""

    if request.method == "POST":
        length = int(request.form["length"])

        if request.form.get("upper"):
            chars += string.ascii_uppercase
        if request.form.get("lower"):
            chars += string.ascii_lowercase
        if request.form.get("digits"):
            chars += string.digits
        if request.form.get("symbols"):
            chars += string.punctuation

        password = ''.join(random.choice(chars) for _ in range(length))

        conn = sqlite3.connect("passwords.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO history VALUES (?)", (password,))
        conn.commit()
        conn.close()

    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()
    cur.execute("SELECT password FROM history ORDER BY ROWID DESC LIMIT 5")
    history = [row[0] for row in cur.fetchall()]
    conn.close()

    return render_template("index.html", password=password, history=history)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
