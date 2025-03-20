from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)
app.secret_key = "venkat"  # Required for flashing messages

# Function to connect to MySQL database
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Route to display the form and user data
@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    if not conn:
        return "Database connection failed!"

    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        branch = request.form["branch"].strip()
        age = request.form["age"].strip()
        sex = request.form["sex"]

        if name and email and branch and age and sex:
            try:
                cursor.execute(
                    "INSERT INTO users (name, email, branch, age, sex) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, branch, age, sex)
                )
                conn.commit()
                flash("User added successfully!", "success")
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
        else:
            flash("All fields are required!", "warning")

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", users=users)

# Route to update user details
@app.route("/update/<int:id>", methods=["POST"])
def update_user(id):
    name = request.form["name"].strip()
    email = request.form["email"].strip()
    branch = request.form["branch"].strip()
    age = request.form["age"].strip()
    sex = request.form["sex"]

    conn = get_db_connection()
    if not conn:
        return "Database connection failed!"

    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE users SET name = %s, email = %s, branch = %s, age = %s, sex = %s WHERE id = %s",
            (name, email, branch, age, sex, id)
        )
        conn.commit()
        flash("User updated successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error updating user: {err}", "danger")

    cursor.close()
    conn.close()

    return redirect(url_for("index"))

# Route to delete a user
@app.route("/delete/<int:id>")
def delete_user(id):
    conn = get_db_connection()
    if not conn:
        return "Database connection failed!"

    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        flash("User deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error deleting user: {err}", "danger")

    cursor.close()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
