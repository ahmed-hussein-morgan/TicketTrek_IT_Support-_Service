from flask import Flask


# The __name__ argument that is passed to the Flask application constructor:
# Flask uses this argument to determine the location of the application, 
# which in turn allows it to locate other files that are part of the application,
#  (such as images and templates).
# 
# To run the application and activate the Debug mood Automatically :
# (venv) $ export FLASK_APP=simple_ticket.py
# (venv) $ export FLASK_DEBUG=1
# (venv) $ flask run
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"