# install needed packages below using pip
from flask import Flask, render_template
#replace the boostrap by JQuery or normal JavaScript
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from flask_login import LoginManager


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.register_blueprint(main_blueprint)
    # The url_prefix argument in the blueprint registration is optional
    # When used, all the routes defined in the blueprint will be registered with the given prefix,
    # in this case /auth
    # For example, the /login route will be registered as /auth/login
    # and the fully qualified URL under the development web server then becomes http://localhost:5000/auth/login
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # attach routes and custom error pages here

    return app