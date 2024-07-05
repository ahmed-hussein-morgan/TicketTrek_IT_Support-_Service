from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors



# the the correct code of the below function in application’s Git repository on GitHub
# This change is shown in Example 9-8
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)