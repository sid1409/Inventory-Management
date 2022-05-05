#Imports
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from requests import session
from werkzeug.security import generate_password_hash, check_password_hash
from validators import *

#Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3' #TODO Change DB on release
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Models
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

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
    )
    inv_type = db.Column(
        db.String(100),
        nullable=False,
    )
    no_of_pro = db.Column(
        db.Integer,
        nullable = False
    )
    manuDate = db.Column(
        db.Integer,
        nullable = True
    )
    expDate = db.Column(
        db.Integer,
        nullable = True
    )
    price = db.Column(
        db.Float,
        nullable = False
    )

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique = True
    )

#Routes
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
    return render_template('login.html')

@app.route('/loginShow')
def showLoginPage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    retailer_id = request.form['id']
    retailer_pass = request.form['password']
    
    res = None
    session = dict()
    session['userFound'] = True
    with db.engine.connect() as conn:
        curr = conn.execute("SELECT name, password FROM 'retailer-info' WHERE name = '{}';".format(retailer_id))
        res = curr.fetchone()
    
    if res == None or not check_password_hash(res[1], retailer_pass):
        session['userFound'] = False
        return render_template('login.html', session = session)
    else:
        session['user'] = res[0]
    return render_template('header.html', session = session)


@app.route('/showAddInv')
def showAddInv():
    listOfInv = []
    temp = []
    session = dict()
    with db.engine.connect() as conn:
        curr = conn.execute("SELECT name FROM 'inventory';")
        temp = curr.fetchall()
    if temp != None:
        for all in temp:
            listOfInv.append(all[0])
    session['listOfInv'] = listOfInv

    return render_template('addInv.html', session = session)


@app.route('/addInv', methods = ['POST'])
def addInv():
    session = dict()
    inv = Inventory()
    inv.name = str(request.form['inv_type']).lower()

    db.session.add(inv)
    db.session.commit()

    listOfInv = []
    temp = []
    with db.engine.connect() as conn:
        curr = conn.execute("SELECT name FROM 'inventory';")
        temp = curr.fetchall()
    if temp != None:
        for all in temp:
            listOfInv.append(all[0])
    session['listOfInv'] = listOfInv

    return render_template('addInv.html', session = session)

@app.route('/showAddPro')
def showAddPro():
    listOfInv = []
    temp = []
    session = dict()
    with db.engine.connect() as conn:
        curr = conn.execute("SELECT name FROM 'inventory';")
        temp = curr.fetchall()
    if temp != None:
        for all in temp:
            listOfInv.append(all[0])
    session['listOfInv'] = listOfInv
    return render_template('addPro.html', session = session)

@app.route('/addPro', methods=['POST'])
def addPro():
    pro = Product()
    pro.inv_type = request.form['inv_type']
    pro.name = str(request.form['proName']).lower()
    pro.no_of_pro = int(request.form['noOfProducts'])
    pro.manuDate = request.form['manuDate']
    pro.expDate = request.form['expDate']
    pro.price = float(request.form['price'])

    db.session.add(pro)
    db.session.commit()
    return render_template('addPro.html')

@app.route('/showAltPri')
def showAltPri():
    return render_template('altPri.html')

@app.route('/altPri')
def alrPri():
    #TODO
    return render_template('addPro.html')

@app.route('/showGenRep')
def showGenRep():
    return render_template('genReport.html')

@app.route('/genReport')
def genReport():
    #TODO
    return render_template()

@app.route('/showSetAlert')
def showSetAlert():
    return render_template('setAlert.html')
@app.route('/setAlert')
def setAlert():
    #TODO
    return render_template('setAlert.html')

if __name__ == "__main__":
    app.run(debug=True) #TODO remove debug on release