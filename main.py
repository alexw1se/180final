from flask import Flask, render_template, request, flash, redirect, url_for, session
from sqlalchemy import create_engine, text
from passlib.hash import sha256_crypt
from sqlalchemy.testing import db
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn_str = "mysql+pymysql://root:Savier010523$@localhost/Vendor_App"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('home.html', email=session.get('email'))
    else:
        return redirect(url_for('login'))

@app.route('/myaccount')
def myaccount():
    if 'logged_in' in session and session['logged_in']:
        user_email = session['email']
        with engine.connect() as conn:
            user_data = conn.execute(text("SELECT * FROM register WHERE email = :email"), {'email': user_email}).fetchone()
        if user_data:
            return render_template('myaccount.html', user=user_data)
        else:
            flash('User not found.')
            return redirect(url_for('login'))
    else:
        flash('You need to log in to access your account.')
        return redirect(url_for('login'))
    
@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')

    conn = engine.connect()
    conn.execute(text(
        'INSERT INTO Register (Username, Firstname, Lastname, Email, Passwords) VALUES (:Username, :Firstname, '
        ':Lastname, :Email, :Passwords)'),
        {'Username': username, 'Firstname': firstname, 'Lastname': lastname, 'Email': email,
         'Passwords': password})
    conn.commit()
    conn.close()

    flash('Registration Successful!')
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = engine.connect()
        user = conn.execute(text("SELECT * FROM Register WHERE Email = :email"),
                            {'email': email}).first()
        conn.close()
        if user:
            stored_password = user[5]
            if stored_password == password:
                session['logged_in'] = True
                session['email'] = email  # Set the session.email variable
                session['Username'] = user[1]  # Set the session.Username variable
                flash('Login Successful!')
                return redirect(url_for('home'))
            else:
                flash('Invalid password. Please try again.')
                return render_template('login.html')
        else:
            flash('Invalid email. Please try again.')
            return render_template('register.html')

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))




@app.route('/register')
def register():
    return render_template('register.html')



messages = []

#Chat


def add_product_form():
     return render_template("add_product.html")

def add_productd():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        description = request.form.get('description')
        inventory = request.form.get('inventory')
        colors = request.form.get('colors')
        size = request.form.get('size')
        warranty_period = request.form.get('warranty_period')
        vendor_id = request.form.get('vendor_id')

        conn = engine.connect()
        conn.execute(text(
            "INSERT into product (Product_title, Product_price, Product_description, inventory, Product_colors, Product_size, warranty_period, VendorID) VALUES (:title, :price, :description, :inventory, :colors, :size, :warranty_period, :vendor_id"),
            {'title':title, 'price':price, 'description':description,'inventory':inventory,'colors':colors,'size':size, 'warranty_period':warranty_period,'vendor_id':vendor_id})
        conn.close()

        flash('Product Added Successfully!')
        #for now redirect to home, but change to cart or extendd admin page, idk yet
        return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
