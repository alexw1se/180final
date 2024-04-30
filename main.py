from flask import Flask, render_template, request, flash, redirect, url_for, session
from sqlalchemy import create_engine, text
from passlib.hash import sha256_crypt
from sqlalchemy.testing import db
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn_str = "mysql+pymysql://root:mlcset1555@localhost/Vendor_App"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/myaccount')
def myaccount():
    if 'logged_in' in session and session['logged_in']:
        if 'username' in session:
            username = session['username']
            user_email = session['user_email']
            return render_template("myaccount.html", username=username, user_email=user_email)
        else:
            flash('User information not found. Please log in again')
            return redirect(url_for('login'))
    else:
        flash('You need to log in to access your account.')
        return redirect(url_for('login'))


@app.route('/register', methods=['GET'])
def register_get():
    return render_template("register.html")


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

@app.route('/login_get')
def login_get():
    return render_template('login.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = engine.connect()
        user = conn.execute(text("SELECT * FROM Register WHERE Email = :email AND Passwords = :password"),
                            {'email': email, 'password': password}).first()
        conn.close()

        if user:
            session['logged_in'] = True
            if 'Email' in user:
                session['user_email'] = user['Email']
                username = conn.execute(text("SELECT Username FROM Register WHERE Email = :email"),
                                        {'email': email}).scalar()
                if username:
                    session['username'] = username
                flash('Login Successful!')
                return render_template('myaccount.html', user=user)

    return render_template('myaccount.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))


# Login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('Email')
#         passwords = request.form.get('Passwords')
#
#         user = Register.query.filter_by(Email=email).first()
#         if user and check_password_hash(user.Passwords, passwords):
#             flash('Login successful.')
#             return redirect(url_for('home'))
#
#     return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


messages = []

#Chat
@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/chat', defaults={'chat_type': 'returns'})
@app.route('/chat/<chat_type>')
def index(chat_type):

@app.route('/', methods=['GET', 'POST'])
def chat():

    if request.method == 'POST':
        chat_type = request.form.get('chat_type')
        message = request.form.get('message')
        dates = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        customer_id = request.form.get('CustomerID')

        try:
            with engine.connect() as connection:
                result = connection.execute(text("INSERT INTO messages (dates, CustomerID, message, chat_type) VALUES (:dates, :CustomerID, :message, :chat_type)"),
                                            {"dates": dates, "CustomerID": customer_id, "message": message, "chat_type": chat_type})
        except Exception as e:
            print(f"Error inserting message: {e}")
            return "Error inserting message", 500

        return redirect(url_for('chat', chat_type=chat_type))

    chat_type = request.args.get('chat_type', 'general')
    try:
        with engine.connect() as connection:

            connection.execute(text(
                "INSERT INTO Chat (message, dates, CustomerID, chat_type) VALUES (:message, :date, :customer_id, :chat_type)"),
                               message=message, date=date, customer_id=customer_id, chat_type=chat_type)

    with engine.connect() as connection:
        messages = connection.execute(text("SELECT * FROM Chat WHERE chat_type = :chat_type"),
                                      chat_type=chat_type).fetchall()

            result = connection.execute(text("SELECT * FROM messages WHERE chat_type = :chat_type"), {"chat_type": chat_type})
            messages = result.fetchall()
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return "Error fetching messages", 500


    return render_template('chat.html', chat_type=chat_type, messages=messages)


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
