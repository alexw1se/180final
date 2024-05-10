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
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route('/myaccount')
def myaccount():
    if 'logged_in' in session and session['logged_in']:
        user = session['email'] 
        return render_template('myaccount.html', user=user)
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
                session['email'] = email
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
    flash('You have been logged out.')
    return redirect(url_for('home'))




@app.route('/register')
def register():
    return render_template('register.html')



messages = []

#Chat
@app.route('/chat', methods=['GET', 'POST'])
def chat():

    if request.method == 'POST':
        customer_message = request.form.get('message')
        customer_id = session.get('customer_id')
        chat_type = 'customer_service'
        dates = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            with engine.connect() as connection:
                connection.execute(text("INSERT INTO Chat (dates, CustomerID, message, chat_type) VALUES (:dates, :CustomerID, :message, :chat_type)"),
                {'dates':dates,'CustomerID':customer_id,'message':customer_message,'chat_type':chat_type})

        except Exception as e:
            flash('an error occurred, try later')
            print(e)


    chat_history=[]
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM Chat WHERE CustomerID = :customer_id"), {'customer_id':customer_id})
            chat_history = result.fetchall()
    except Exception as e:
        flash('error occurred, try again')
        print(e)

    return render_template('chat.html', chat_history=chat_history)



    return render_template('chat.html', chat_type=chat_type, messages=messages)



def add_product_form():
     return render_template('add_product.html')

def add_product():
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
