from flask import Flask, redirect, render_template, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Application Setup
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
def index():
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
    if 'user_id' not in session:
        flash("Please Login First!", "error")
        return render_template("login.html")
    
    with get_db_connection() as connection:
        user = connection.execute('''
            SELECT * FROM cartUsers where id=?
        ''', (session['user_id'],)
        ).fetchone()

        connection.commit()

    return render_template('home.html', user=dict(user))


# Add to Cart Route
@app.route('/add_to_cart', methods=["GET", "POST"])
def add_to_cart():
    if 'user_id' not in session:
        flash("Please Login First!", "error")
        return render_template("login.html")
    
    if request.method == "POST":
        user_id = session['user_id']
        product_name = request.form["name"]
        price = float(request.form["price"])
        quantity = int(request.form['quantity'])

        with get_db_connection() as connection:
            existing = connection.execute('''
                SELECT quantity FROM cart WHERE user_id=? AND product_name=?
            ''', (user_id, product_name)).fetchone()

            if existing:
                new_quantity = existing['quantity'] + quantity
                new_total = price * new_quantity
                connection.execute('''
                    UPDATE cart
                    SET quantity = ?, total = ?
                    WHERE user_id=? AND product_name=?
                ''', (new_quantity, new_total, user_id, product_name))
            else:
                total = price * quantity
                connection.execute('''
                    INSERT INTO cart (user_id, product_name, price, quantity, total)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, product_name, price, quantity, total))

            connection.commit()

    flash("Added Item to Cart!", "success")
    return redirect(url_for("dashboard"))


# View Cart Route
@app.route('/view_cart')
def view_cart():
    if "user_id" not in session:
        flash("Please login first!", "error")
        return render_template("login.html")

    user_id = session['user_id']

    with get_db_connection() as connection:
        cart = connection.execute('''
            SELECT user_id, product_name, price, quantity, total
            FROM cart
            WHERE user_id=?
        ''', (user_id,)).fetchall() or 0 

        grand_total = 0

        if cart:
            cart = [dict(row) for row in cart]
            for item in cart:
                item['total'] = int(item['price']) * int(item['quantity'])
                grand_total += item['total']

    return render_template('view-cart.html', cart=cart, grand_total=grand_total)


# Remove from cart Route
@app.route('/RemoveFromCart/<product_name>', methods=["GET", "POST"])
def remove(product_name):
    if 'user_id' not in session:
        flash("Please loging first!", "error")
    
    user_id = session['user_id']
    if request.method == "POST":
        with get_db_connection() as connection:
            connection.execute('''
                DELETE FROM cart 
                WHERE product_name=? AND user_id=?
            ''', (product_name, user_id)
            )

            connection.commit()
    
    flash(f"Removed {product_name} from cart successfully!", "success")
    return redirect(url_for("view_cart"))


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    
    flash("Logout Successful!", "success")
    return redirect(url_for('login'))


# Main Entry
if __name__ == '__main__':
    app.run(debug=True)