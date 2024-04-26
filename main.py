from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
from datetime import datetime

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
            result = connection.execute(text("SELECT * FROM messages WHERE chat_type = :chat_type"), {"chat_type": chat_type})
            messages = result.fetchall()
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return "Error fetching messages", 500

    return render_template('chat.html', chat_type=chat_type, messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
