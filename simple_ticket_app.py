from flask import Flask, render_template, url_for, current_app, g, request, session,redirect

# current_app: The application instance for the active application. - this is related to the Application context
# g: An object that the application can use for temporary storage during the handling of a request. This variable is reset with each request.
#     - this is related to the Application context
# request: The request object, which encapsulates the contents of an HTTP request sent by the client.
#     - this is related to the Request context
# session: The user session, a dictionary that the application can use to store values that are “remembered” between requests.
#     - this is related to the Request context

from datetime import datetime, timezone
# from flask_moment import Moment


app = Flask(__name__)
# moment = Moment(app)

# @app.route("/")
@app.route("/home")
@app.route('/')
def home():
    # return render_template("home.html", title="Home", current_time=datetime.utcnow())
    return render_template("home.html", title="Home", current_time=datetime.now())

@app.route("/about")
def about():
    return render_template("about.html", title="About Us")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Us")



if __name__ == "__main__":
    app.run(debug=True)
