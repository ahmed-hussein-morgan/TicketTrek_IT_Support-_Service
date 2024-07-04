from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from DBstorage import User


class RegistrationForm(FlaskForm):
    """
    A class to represent a registration form for new users.

    Attributes:
    - username (StringField): Field for entering the username with validators for data required and length constraints.
    - email (StringField): Field for entering the email address with validators for data required and email format.
    - password (PasswordField): Field for entering the password with a validator for data required.
    - confirm_password (PasswordField): Field for confirming the password with a validator to ensure it matches the password field.
    - submit (SubmitField): Button field for submitting the registration form.

    Methods:
    - validate_username(self, username): Method to validate the uniqueness of the entered username by checking against existing users in the database.
    - validate_email(self, email): Method to validate the uniqueness of the entered email by checking against existing users in the database.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """
    A class to represent a login form for existing users.

    Attributes:
    - email (StringField): Field for entering the email address with validators for data required and email format.
    - password (PasswordField): Field for entering the password with a validator for data required.
    - remember (BooleanField): Field for allowing users to choose whether to be remembered for the next login session.
    - submit (SubmitField): Button field for submitting the login form.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    A class to represent a form for updating user account information.

    Attributes:
    - username (StringField): Field for entering the username with validators for data required and length constraints.
    - email (StringField): Field for entering the email with validators for data required and email format.
    - picture (FileField): Field for updating the profile picture with validators for allowed file types.
    - submit (SubmitField): Button field for submitting the form.

    Methods:
    - validate_username(self, username): Custom validation method to check if the entered username is unique.
    - validate_email(self, email): Custom validation method to check if the entered email is unique.

    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    """
    A class to represent a form for requesting a password reset.

    Attributes:
    email (StringField): A field for entering the email address.
    submit (SubmitField): A button to submit the password reset request.

    Methods:
    validate_email(self, email): Validates the email address entered in the form by checking if it exists in the database.

    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """
    A class to represent a form for resetting the user's password.

    Attributes:
    - password (PasswordField): Field for entering the new password with a validator for data required.
    - confirm_password (PasswordField): Field for confirming the new password with a validator to ensure it matches the password field.
    - submit (SubmitField): Button field for submitting the password reset form.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
