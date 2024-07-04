from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from __init__ import db, login_manager
from sqlalchemy import Enum, CheckConstraint
import enum
    

class Role(enum.Enum):
    USER = 'User'
    IT = 'IT'

class User(db.Model, UserMixin):
    """
    A class to represent a User in the database.

    Attributes:
    id (int): The primary key of the user.
    username (str): The username of the user.
    email (str): The email address of the user.
    image_file (str): The file path for the user's profile image.
    password (str): The hashed password of the user.
    role (Enum): The role of the user (User or IT).
    tickets (relationship): The tickets associated with the user.

    Methods:
    get_reset_token(expires_sec=1800): Generate a token for resetting the user's password.
    verify_reset_token(token): Verify and return the user based on the reset token.
    __repr__(): Return a printable representation of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(Enum(Role), nullable=False)
    tickets = db.relationship('Ticket', backref='author', lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        """
        Generate a token for resetting the user's password.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
  
     
class Ticket(db.Model):
    """
    Class representing a ticket in the TicketTrek IT Support Service.

    Attributes:
    ticket_id (int): The unique identifier for the ticket.
    ticket_title (str): The title of the ticket.
    date_posted (datetime): The date and time when the ticket was posted.
    content (str): The content or description of the ticket.
    user_id (int): The foreign key referencing the user who created the ticket.

    Table Constraints:
    CheckConstraint: Ensures that the role associated with the ticket is 'User'.

    Methods:
    __repr__: Returns a string representation of the ticket object.

    """
    ticket_id = db.Column(db.Integer, primary_key=True)
    ticket_title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __table_args__ = (
        CheckConstraint('(Role = \'User\')'),
    )

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
 
class Response(db.Model):
    """
    A class to represent a response in the database.

    Attributes:
    id (int): The primary key of the response.
    date_posted (datetime): The date and time when the response was posted.
    content (str): The content of the response.
    user_id (int): The foreign key referencing the user who posted the response.

    Table Constraints:
    Role (str): The role of the user posting the response must be 'IT'.

    Methods:
    __repr__: Returns a string representation of the response object.

    """
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __table_args__ = (
        CheckConstraint('(Role = \'IT\')'),
    )

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"   
    
@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user from the database based on the user_id.

    Parameters:
    user_id (int): The ID of the user to load.

    Returns:
    User: The User object corresponding to the user_id.
    """
    return User.query.get(int(user_id))
