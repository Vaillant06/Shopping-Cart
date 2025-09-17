from flask import Flask, redirect, render_template, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

DB_NAME = 'ShoppingCart.db'
app = Flask(__name__)
app.secret_key = 'mySecretKey'


# Database connection helper
def get_db_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection   


# Landing Route
@app.route('/')
def home():
    return render_template('index.html')


# Login route
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        with get_db_connection() as connection:
            user = connection.execute(
                "SELECT * FROM cartUsers WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user["password"], password): 
            session["user_id"] = user["id"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password!", "error")
        return redirect(url_for('login'))

    return render_template('login.html')


# Register Route
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        phone = request.form["phone"]
        raw_password = request.form["password"]
        confirm_raw_password = request.form["confirm-password"]

        if raw_password != confirm_raw_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))
        
        hashed_pw = generate_password_hash(raw_password)

        with get_db_connection() as connection:
            if connection.execute("SELECT 1 FROM cartUsers WHERE username=?", (username,)).fetchone():
                flash("Username already exists!", "error")
                return redirect(url_for('register'))
            
            if connection.execute("SELECT 1 FROM cartUsers WHERE phone_number=?", (phone,)).fetchone():
                flash("Phone number exists!", "error")
                return redirect(url_for('register')) 

            hashed_pw = generate_password_hash(raw_password)
            connection.execute(
                '''INSERT INTO CartUsers (username, phone_number, password) VALUES (?, ?, ?)''',
                (username, phone, hashed_pw),
            )
            connection.commit()
        
        flash("Registration Successful. You can login!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('home.html')


# View Cart Route
@app.route('/view_cart')
def view_cart():
    return render_template('view-cart.html')


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    
    flash("Logout Successful!", "success")
    return redirect(url_for('login'))


# Main Entry
if __name__ == '__main__':
    app.run(debug=True)