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
    """
    Route for creating a new Ticket.
    This function is decorated with the `@login_required` decorator, which means that the user must be authenticated to access this route.
    The function first creates a new instance of the `TicketForm` class.
    If the form is valid (i.e., all the required fields are filled in correctly), the function creates a new `Ticket` object with the provided title, content, and the current user as the author.
    The new `Ticket` object is then added to the database and committed to the session.
    A success flash message is displayed and the user is redirected to the home page.
    If the form is not valid, the function renders the `create_Ticket.html` template with the provided title, form, and legend.

    Returns:
    - If the form is valid, a redirect to the home page.
    - If the form is not valid, a rendered template.

    """
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
    """
    Route for displaying the details of a specific ticket.

    Parameters:
    Ticket_id (int): The ID of the ticket to be displayed.

    Returns:
    flask.Response: The rendered template 'Ticket.html' with the ticket details.
    """
    Ticket = Ticket.query.get_or_404(Ticket_id)
    return render_template('Ticket.html', title=Ticket.title, Ticket=Ticket)


@Tickets.route("/Ticket/<int:Ticket_id>/update", methods=['GET', 'POST'])
@login_required
def update_Ticket(Ticket_id):
    """
    A route for updating a specific ticket based on the Ticket_id.
    If the user is not the author of the ticket, abort with status code 403.
    Creates a form for updating the ticket and validates the form data.
    If the form is valid, updates the ticket title and content in the database.
    Flashes a success message and redirects to the updated ticket details page.
    If the request method is 'GET', pre-populates the form with the existing ticket data.
    Renders the 'create_Ticket.html' template for updating a ticket.
    """
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
    """
    Deletes a ticket with the given Ticket_id.

    Parameters:
    Ticket_id (int): The ID of the ticket to be deleted.

    Returns:
    flask.Response: A redirect to the main home page.

    Raises:
    HTTPException: If the current user is not the author of the ticket.
    """
    Ticket = Ticket.query.get_or_404(Ticket_id)
    if Ticket.author != current_user:
        abort(403)
    db.session.delete(Ticket)
    db.session.commit()
    flash('Your Ticket has been deleted!', 'success')
    return redirect(url_for('main.home'))
