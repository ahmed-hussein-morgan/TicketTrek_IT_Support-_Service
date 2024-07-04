from flask import render_template, request, Blueprint
from models.DBstorage import Ticket

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    Tickets = Ticket.query.order_by(Ticket.date_Ticketed.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', Tickets=Tickets)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
