from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class TicketForm(FlaskForm):
    """
    A class representing a form for submitting tickets.

    Attributes:
    title (StringField): A field for entering the title of the ticket.
    content (TextAreaField): A field for entering the content of the ticket.
    submit (SubmitField): A button for submitting the ticket.
    """
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class ResponseForm(FlaskForm):
    """
    A class representing a form for submitting responses.

    Attributes:
    content (TextAreaField): A field for entering the content of the response.
    submit (SubmitField): A button for submitting the response.

    """
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
