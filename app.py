from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from validators import *

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
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

@app.route('/signUp', methods = ['POST'])
def signUp():
    retailer_id = request.form['id']
    retailer_email = request.form['email']
    retailer_pass = request.form['password']
    retailer_repass = request.form['repassword']
    session = dict()

    session['nameError'] = nameValidator(retailer_id)
    session['emailError'] = emailValidator(retailer_email)
    session['passError'] = passValidator(retailer_pass)
    session['rePassError'] = (retailer_repass == retailer_pass)

    if not (session['passError'] and session['emailError'] and session['nameError'] and session['rePassError']):
        return render_template('signup.html', session = session)

    retailer = Retailer()
    retailer.name = retailer_id
    retailer.email = retailer_email
    retailer.password = generate_password_hash(retailer_pass, "sha256")

    db.session.add(retailer)
    db.session.commit()




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