import os

class Config:
    """
    A class to store configuration settings for the application.

    Attributes:
    SECRET_KEY (str): The secret key for the application.
    SQLALCHEMY_DATABASE_URI (str): The URI for the SQL database.
    MAIL_SERVER (str): The SMTP server for sending emails.
    MAIL_PORT (int): The port for the email server.
    MAIL_USE_TLS (bool): Whether to use TLS for email communication.
    MAIL_USERNAME (str): The username for the email server.
    MAIL_PASSWORD (str): The password for the email server.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
