from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

conn_str = "mysql://root:Savier010523$@localhost/Vendor_App"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def home():
    return render_template("home.html")




@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

messages = []

@app.route('/chat')
def chat():
	return render_template('chat.html')

@app.route('/chat', defaults={'chat_type': 'returns'})
@app.route('/chat/<chat_type>')
def index(chat_type):
    if request.method == 'POST':
        message = request.form['message']
        customer_id = 1
        date = datetime.datetime.now()

        with engine.connect() as connection:
            connection.execute(text("INSERT INTO Chat (message, dates, CustomerID, chat_type) VALUES (:message, :date, :customer_id, :chat_type)"), message=message, date=date, customer_id=customer_id, chat_type=chat_type)

    with engine.connect() as connection:
        messages = connection.execute(text("SELECT * FROM Chat WHERE chat_type = :chat_type"), chat_type=chat_type).fetchall()

    return render_template('index.html', messages=messages, chat_type=chat_type)

if __name__ == '__main__':
    app.run(debug=True)
