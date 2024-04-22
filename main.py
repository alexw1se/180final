from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

# connection string is in the format mysql://user:password@server/database
conn_str = "mysql+pymysql://root:@localhost/Vendor_App"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def home():
    return render_template("home.html")


# @app.route('/login')
# def get_boats():
#     boats = conn.execute(text("select * from boats")).all()
#     return render_template("boats.html", boats_info=boats[:10])
#
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
    # ... start the app in debug mode. In debug mode,
    # server is automatically restarted when you make changes to the code