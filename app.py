from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Retailer(db.Model):
    __tablename__ = 'retailer-info'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)

@app.route('/')
def hello_world():
    return render_template('index.html')



@app.route('/signUpShow')
def showSignUpPage():
    return render_template('signup.html')

@app.route('/signUp')
def signUp():
    retailer_id = request.form['id']
    retailer_pass = request.form['password']
    retailer = Retailer()
    #TODO: check ID and Password from database



@app.route('/loginShow')
def showLoginPage():
    return render_template('login.html')

@app.route('/login')
def login():
    retailer_id = request.form['id']
    retailer_pass = request.form['password']
    #TODO: check ID and Password from database

if __name__ == "__main__":
    app.run(debug=True)