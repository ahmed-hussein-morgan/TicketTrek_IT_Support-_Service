from flask import Flask, render_template, url_for, current_app, g, request, session,redirect, flash

# current_app: The application instance for the active application. - this is related to the Application context
# g: An object that the application can use for temporary storage during the handling of a request. This variable is reset with each request.
#     - this is related to the Application context
# request: The request object, which encapsulates the contents of an HTTP request sent by the client.
#     - this is related to the Request context
# session: The user session, a dictionary that the application can use to store values that are “remembered” between requests.
#     - this is related to the Request context

from datetime import datetime, timezone, date, time
from forms import RegistrationForm, LoginForm

# import the SQLALchemy to start working with database (mysql in this case)
from flask_sqlalchemy import SQLAlchemy


from sqlalchemy.sql.expression import func

from enum import Enum

import os


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# app.config['MYSQL_HOST'] = os.environ.get('HOST')
app.config['MYSQL_USER'] = os.environ.get('DBUSER')
app.config['MYSQL_PASSWORD'] = os.environ.get('DBPASSWORD')
app.config['MYSQL_DB'] = os.environ.get('SIMPLEDB')

# configure the Database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}@localhost/{app.config['MYSQL_DB']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Another way to configure the database by using .forma() insteaf of the python f-string is below:
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}/{}".format(
#     app.config['MYSQL_USER'], 
#     app.config['MYSQL_PASSWORD'], 
#     app.config['MYSQL_HOST'], 
#     app.config['MYSQL_DB']
# )

# create an instance of the database to b ready to work with it
db = SQLAlchemy(app)


# creating the database tables

class RoleType(Enum):
    TECH = "tech"
    NON_TECH = "non-tech"

class TicketStatus(Enum):
    OPEN = "open"
    RECEIVED = "received"
    SOLVED = "solved"

class TicketType(Enum):
    REQUEST = "request"
    COMPLAIN = "complain"


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    role_type = db.Column(db.Enum(RoleType), nullable=False)
    # users = db.relationship("User", backref="role", lazy=True)
    users = db.relationship("User", backref=db.backref("role", lazy=True))


class User(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    employee_name = db.Column(db.String(20), nullable=False, unique=True)
    department = db.Column(db.String(20), nullable=False)
    job_title = db.Column(db.String(20), nullable=False)
    role_type_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    branch = db.Column(db.String(30), nullable=False)
    # roles = db.relationship("Role", backref="user")

class Ticket(db.Model):
    __tablename__ = "tickets"
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    ticket_type = db.Column(db.Enum(TicketType), nullable=False)
    # ticket_category = db.Column(db.String(64), nullable=False) could be changed on productuon to be "enum" with limited category list
    ticket_category = db.Column(db.String(30), nullable=False)
    ticket_title = db.Column(db.String(64), nullable=False)
    ticket_details = db.Column(db.Text, nullable=False)

    # Adding a column to add attached files like photos or screenshots (Canceled)because:
    #       it either need an additional cost to store these files on a cloud 

    # Pause for implementing the attachment now
    # ticket_attachment = db.Column(db.)

    submission_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
    # submission_time = db.Column(db.Time, nullable=False, default=func.now().time())
    ticket_status = db.Column(db.Enum(TicketStatus), nullable=False)
    # tickets = db.relationship("IT", backref="ticket")
    tickets = db.relationship("IT", backref=db.backref("ticket", lazy=True))



class IT(db.Model):
    __tablename__ = "it_tickets"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    tech_name = db.Column(db.String(30), nullable=True)
    update_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
    # update_time = db.Column(db.Time, nullable=False, default=func.now().time())
    update_ticket_details = db.Column(db.Text, nullable=True)

class UserTicket(db.Model):
    __tablename__ = "employee_ticket"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    


# @app.route("/")
@app.route("/home")
@app.route('/')
def home():
    # return render_template("home.html", title="Home", current_time=datetime.utcnow())
    return render_template("home.html", title="Home", current_time=datetime.now())

@app.route("/about")
def about():
    return render_template("about.html", title="About Us")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "ahmed" and form.password.data == "123456":
            flash(f"Login Successfully {form.username.data}!", "sucess")
            session["name"] = form.username.data
            return redirect(url_for("home"))
        else:
            flash("Unsuccessful Login. Please check your username and password", "danger")
    return render_template("login.html", title="Login", form=form, name=session.get('name'))



@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Us")



if __name__ == "__main__":
    app.run(debug=True)
