from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from __init__ import db
from models.DBstorage import Ticket
from models.TicketForms import TicketForm

Tickets = Blueprint('Tickets', __name__)


@Tickets.route("/Ticket/new", methods=['GET', 'POST'])
@login_required
def new_Ticket():
    form = TicketForm()
    if form.validate_on_submit():
        Ticket = Ticket(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(Ticket)
        db.session.commit()
        flash('Your Ticket has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_Ticket.html', title='New Ticket',
                           form=form, legend='New Ticket')


@Tickets.route("/Ticket/<int:Ticket_id>")
def Ticket(Ticket_id):
    Ticket = Ticket.query.get_or_404(Ticket_id)
    return render_template('Ticket.html', title=Ticket.title, Ticket=Ticket)


@Tickets.route("/Ticket/<int:Ticket_id>/update", methods=['GET', 'POST'])
@login_required
def update_Ticket(Ticket_id):
    Ticket = Ticket.query.get_or_404(Ticket_id)
    if Ticket.author != current_user:
        abort(403)
    form = TicketForm()
    if form.validate_on_submit():
        Ticket.title = form.title.data
        Ticket.content = form.content.data
        db.session.commit()
        flash('Your Ticket has been updated!', 'success')
        return redirect(url_for('Tickets.Ticket', Ticket_id=Ticket.id))
    elif request.method == 'GET':
        form.title.data = Ticket.title
        form.content.data = Ticket.content
    return render_template('create_Ticket.html', title='Update Ticket',
                           form=form, legend='Update Ticket')


@Tickets.route("/Ticket/<int:Ticket_id>/delete", methods=['POST'])
@login_required
def delete_Ticket(Ticket_id):
    Ticket = Ticket.query.get_or_404(Ticket_id)
    if Ticket.author != current_user:
        abort(403)
    db.session.delete(Ticket)
    db.session.commit()
    flash('Your Ticket has been deleted!', 'success')
    return redirect(url_for('main.home'))
