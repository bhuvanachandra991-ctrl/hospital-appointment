from flask import Flask, render_template, request
import sqlite3
from datetime import date

app = Flask(__name__)

# -----------------------------
# Create Database
# -----------------------------
def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_date TEXT,
        token INTEGER,
        mobile TEXT,
        name TEXT,
        gender TEXT,
        age INTEGER,
        dob TEXT,
        address TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Submit Patient
# -----------------------------
@app.route("/submit", methods=["POST"])
def submit():

    mobile = request.form["mobile"]
    name = request.form["name"]
    gender = request.form["gender"]
    age = request.form["age"]
    dob = request.form["dob"]
    address = request.form["address"]

    today = date.today().strftime("%Y-%m-%d")

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    # Get today's last token
    cursor.execute(
        "SELECT MAX(token) FROM patients WHERE appointment_date=?",
        (today,)
    )

    result = cursor.fetchone()[0]

    if result is None:
        token = 1
    else:
        token = result + 1

    # Save patient
    cursor.execute("""
    INSERT INTO patients
    (appointment_date, token, mobile, name, gender, age, dob, address)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        today,
        token,
        mobile,
        name,
        gender,
        age,
        dob,
        address
    ))

    conn.commit()
    conn.close()

    return f"""
    <html>
    <head>
    <title>Appointment Successful</title>
    </head>

    <body style="font-family:Arial;text-align:center;background:#f2f2f2;">

        <div style="width:500px;margin:auto;margin-top:60px;
        background:white;padding:30px;border-radius:10px;
        box-shadow:0px 0px 10px gray;">

        <h1 style="color:green;">✔ Appointment Successful</h1>

        <h2>Manikarnika Hospitals</h2>

        <hr>

        <h3>Patient Name</h3>
        <h2>{name}</h2>

        <h3>Appointment Date</h3>
        <h2>{today}</h2>

        <h3>Your Token Number</h3>

        <h1 style="font-size:70px;color:red;">
        {token}
        </h1>

        </div>

    </body>

    </html>
    """
# -----------------------------
# Admin Dashboard
# -----------------------------
@app.route("/admin")
def admin():

    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM patients
    ORDER BY appointment_date DESC, token ASC
    """)

    patients = cursor.fetchall()

    conn.close()

    return render_template("admin.html", patients=patients)
    # -----------------------------
# Run
# -----------------------------
import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )


