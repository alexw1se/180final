from flask import Flask, render_template, request, flash, redirect, url_for, session
from sqlalchemy import create_engine, text
from passlib.hash import sha256_crypt
from sqlalchemy.testing import db
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'


conn_str = "mysql://root:Savier010523$@localhost/Vendor_App"

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

@app.route('/chat', methods=['GET', 'POST'])
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
            result = connection.execute(text("SELECT * FROM messages WHERE chat_type = :chat_type"), {"chat_type": chat_type})
            messages = result.fetchall()
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return "Error fetching messages", 500

    return render_template('chat.html', chat_type=chat_type, messages=messages)

if __name__ == '__main__':
    app.run(debug=True)

