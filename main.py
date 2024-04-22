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
    return render_template("login.html")

#
# @app.route('/register', methods=['GET'])
# def ():
#     return render_template(".html")
#
#
# @app.route('/register', methods=['POST'])
# def ():
#     return render_template(".html")





if __name__ == '__main__':
    app.run(debug=True)
