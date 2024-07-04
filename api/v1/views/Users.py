from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from __init__ import db, bcrypt
from models.DBstorage import User, Ticket
from models.UserForms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from models.UserUtiils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    Route for user registration.
    If the user is already authenticated, redirects to the home page.
    If the registration form is valid, creates a new user with hashed password and adds it to the database.
    If successful, flashes a success message and redirects to the login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, role=form.role.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    Route for user login handling.
    If the user is authenticated, redirects to the home page.
    Validates the login form; if successful, logs the user in.
    If login is successful, redirects to the next page or the home page.
    If login fails, displays an error message.

    Parameters:
    None

    Returns:
    render_template: Renders the login.html template with the login form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    Route for the user account page. Handles form submission to update account details.
    If form validation is successful, updates the user's account information and displays a success message.
    If the request method is 'GET', populates the form with the current user's information.
    Returns the account.html template with the account details and form.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_tickets(username):
    """
    Route for displaying the tickets of a specific user.

    Parameters:
    username (str): The username of the user whose tickets are to be displayed.

    Returns:
    flask.Response: The rendered template 'user_Tickets.html' with the tickets and user information.
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    Tickets = Ticket.query.filter_by(author=user)\
        .order_by(Ticket.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_Tickets.html', Tickets=Tickets, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    Route for resetting the user password using a token.

    Parameters:
    None

    Returns:
    render_template: Renders the reset_request.html with the title 'Reset Password' and the form data.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    Route for resetting the user password using a token.

    Parameters:
    token (str): The token used for resetting the password.

    Returns:
    render_template: Renders the reset_token.html with the title 'Reset Password' and the form data.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
