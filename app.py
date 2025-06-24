from flask import Flask , request , session , render_template, redirect, url_for, flash
# from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, inspect 
from flask_sqlalchemy import SQLAlchemy 
from contact import contact_bp 
from menu import menu_bp , Product
from extensions import db  # centralized file


app =  Flask(__name__)
app.register_blueprint(contact_bp , url_prefix = "")
app.register_blueprint(menu_bp , url_prefix = "/menu")
app.secret_key = "secret_key"
# app.premanent_session_lifetime = timedelta(minutes = 1)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #users : is the class name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # prevent errors

# db = SQLAlchemy(app) #obj from database ,, equall to : new sql database ,, h3ml wahda centralitze
db.init_app(app)


# Initialize the flag to track whether initial products have been added
app.config['INITIAL_PRODUCTS_ADDED'] = False

@app.before_request
def add_initial_products():
    # Check if products have been added
    if not app.config['INITIAL_PRODUCTS_ADDED']:
        # If the products don't exist in the database, add them
        if not Product.query.first():
            db.session.add(Product(name='Latte', price=25, image='static/images/imgg1.jpg'))
            db.session.add(Product(name='Chocolate Mocha', price=25, image='static/images/imgg2.jpg'))
            db.session.add(Product(name='Boba', price=25, image='static/images/imgg3.jpg'))
            db.session.add(Product(name='Espresso', price=25, image='static/images/imgg4.jpg'))
            db.session.add(Product(name='Cinnamon Coffee', price=25, image='static/images/imgg5.jpg'))
            db.session.add(Product(name='Iced Latte', price=25, image='static/images/imgg6.jpg'))
            db.session.commit()
        # Set the flag to True so this block doesn't run again
        app.config['INITIAL_PRODUCTS_ADDED'] = True



class User(db.Model): #table == database model
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    phone = db.Column(db.Integer)



@app.route("/register_user", methods=["POST" , "GET"])
def register():
    print(f"Request method: {request.method}") 
    if request.method == "POST":
        un = request.form["username"]
        pas = request.form["password"]
        phn = request.form["phone"]
        # print(f"Registering User: Username: {un}, Phone: {phn}")  # Debug print

        user_exists = User.query.filter_by(username = un).first() 
        # btgeb elrow elly elusername bta3h "un" kamel
        # user_exist --> maska row

        if user_exists:
            flash("Username already taken. Please try another one.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(pas)
        new_user = User(username=un, password=hashed_password, phone=phn)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        if "username" in session:
            print("Session data:", session)
            return redirect(url_for("home"))

        return render_template("register.html")


@app.route("/")
@app.route("/home")
def home():
    if "username" in session :
        return render_template("home.html")
    else:
        return redirect(url_for("login"))


@app.route("/login" , methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        # session.premanent = False
        un = request.form["username"]
        pas = request.form["password"]

        user_exist = User.query.filter_by(username = un).first() # ba search fel db msh fel session
        if user_exist:
            if check_password_hash(user_exist.password, pas):
                session["username"] = un
                session["password"] = pas
                flash("logged in")
                return redirect(url_for("home"))
            else:
                flash("Invalid password. Please try again.")
                return redirect(url_for("login"))
        else:
            flash("Username not found. Please register.")
            return redirect(url_for("login"))

    else:
        if "username" in session and "password" in session: # we check on the keys if exist , not the values
            return redirect(url_for("home")) # function name , not the route

        return render_template("login.html")


@app.route("/contact us")
def contact():
    return render_template('contact.html')


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)

    # session.clear()  # Clears the entire session
    flash("You have been logged out.")
    return redirect(url_for("login"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables
        inspector = inspect(db.engine)  # Create an inspector
        print("Database tables created:", inspector.get_table_names())  # Print created tables
    app.run(debug=True)










    

