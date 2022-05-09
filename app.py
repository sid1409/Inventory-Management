# Imports
from flask import Flask, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from validators import *

# Config
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "HXW963DGdfSkAD*Ee8*LhZ+"
db = SQLAlchemy(app)


# Models
class Retailer(db.Model):
    __tablename__ = "retailer-info"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(100),
        nullable=False,
    )
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(
        db.String(200), primary_key=False, unique=False, nullable=False
    )


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(100),
        nullable=False,
    )
    inv_type = db.Column(
        db.String(100),
        nullable=False,
    )
    no_of_pro = db.Column(db.Integer, nullable=False)
    manuDate = db.Column(db.Integer, nullable=True)
    expDate = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=False)
    threshold = db.Column(db.Integer, nullable=True)


class Inventory(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


# Routes
@app.route("/")
def hello_world():
    session.clear()
    return render_template("index.html")


@app.route("/home", methods=["GET"])
def home():
    if 'user' in session:
        return render_template("header.html", session=session)
    return redirect(url_for(showLoginPage))


@app.route("/signUpShow")
def showSignUpPage():
    return render_template("signup.html")


@app.route("/signUp", methods=["POST"])
def signUp():
    retailer_id = request.form["id"]
    retailer_email = request.form["email"]
    retailer_pass = request.form["password"]
    retailer_repass = request.form["repassword"]
    session["nameError"] = nameValidator(retailer_id)
    session["emailError"] = emailValidator(retailer_email)
    session["passError"] = passValidator(retailer_pass)
    session["rePassError"] = retailer_repass == retailer_pass
    if not (
        session["passError"]
        and session["emailError"]
        and session["nameError"]
        and session["rePassError"]
    ):
        return render_template("signup.html", session=session)
    retailer = Retailer()
    retailer.name = retailer_id
    retailer.email = retailer_email
    retailer.password = generate_password_hash(retailer_pass, "sha256")
    db.session.add(retailer)
    db.session.commit()
    return render_template("login.html")


@app.route("/loginShow")
def showLoginPage():
    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():

    retailer_id = request.form["id"]
    retailer_pass = request.form["password"]

    res = None
    session["userFound"] = True
    with db.engine.connect() as conn:
        curr = conn.execute(
            "SELECT name, password FROM 'retailer-info' WHERE name = '{}';".format(
                retailer_id
            )
        )
        res = curr.fetchone()

    if res == None or not check_password_hash(res[1], retailer_pass):
        session["userFound"] = False
        return render_template("login.html", session=session)
    else:
        session["user"] = res[0]
    return render_template("header.html", session=session)


@app.route("/showAddInv")
def showAddInv():
    listOfInv = []
    temp = []
    with db.engine.connect() as conn:
        curr = conn.execute("SELECT name FROM 'inventory';")
        temp = curr.fetchall()
    if temp != None:
        for all in temp:
            listOfInv.append(all[0])
    session["listOfInv"] = listOfInv

    return render_template("addInv.html", session=session)


@app.route("/addInv", methods=["POST"])
def addInv():
    inv = Inventory()
    inv.name = str(request.form["inv_type"]).lower()

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
    session["listOfInv"] = listOfInv

    return render_template("addInv.html", session=session)


@app.route("/showAddPro")
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
    session["listOfInv"] = listOfInv
    return render_template("addPro.html", session=session)


@app.route("/addPro", methods=["POST"])
def addPro():
    pro = Product()
    pro.inv_type = request.form["inv_type"]
    pro.name = str(request.form["proName"]).lower()
    pro.no_of_pro = int(request.form["noOfProducts"])
    pro.manuDate = request.form["manuDate"]
    pro.expDate = request.form["expDate"]
    pro.price = float(request.form["price"])
    pro.threshold = 0

    db.session.add(pro)
    db.session.commit()
    return render_template("addPro.html")


@app.route("/showAltPri")
def showAltPri():
    listOfPro = []
    with db.engine.connect() as conn:
        curr = conn.execute("SELECT name, price, expDate FROM 'product';")
        listOfPro = curr.fetchall()
    return render_template("altPri.html", session=session, listOfPro=listOfPro)


@app.route("/altPri", methods=["POST"])
def alrPri():
    with db.engine.connect() as conn:
        curr = conn.execute(
            "UPDATE 'product' SET price = '{}' WHERE name = '{}';".format(
                request.form["price"], request.form["proName"]
            )
        )
    listOfPro = []
    with db.engine.connect() as conn:
        curr = conn.execute("SELECT name, price, expDate FROM 'product';")
        listOfPro = curr.fetchall()
    return render_template("altPri.html", session=session, listOfPro=listOfPro)


@app.route("/showGenRep")
def showGenRep():
    return render_template("genReport.html")


@app.route("/genReport")
def genReport():
    # TODO
    return "<h1>Add More data</h1>"


@app.route("/showSetAlert")
def showSetAlert():
    listOfPro = []
    with db.engine.connect() as conn:
        curr = conn.execute(
            "SELECT name, threshold, no_of_pro, expDate FROM 'product';"
        )
        listOfPro = curr.fetchall()
    return render_template("setAlert.html", session=session, listOfPro=listOfPro)


@app.route("/setAlert", methods=["POST"])
def setAlert():
    threshold = request.form["threshold"]
    with db.engine.connect() as conn:
        curr = conn.execute(
            "UPDATE 'product' SET threshold = '{}' WHERE name = '{}';".format(
                threshold, str(request.form["proName"].lower())
            )
        )
    listOfPro = []
    with db.engine.connect() as conn:
        curr = conn.execute("SELECT name, no_of_pro,threshold, expDate FROM 'product';")
        listOfPro = curr.fetchall()
    return render_template("setAlert.html", session=session, listOfPro=listOfPro)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello_world'))

if __name__ == "__main__":
    app.run()  # TODO remove debug on release
