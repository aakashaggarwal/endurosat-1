from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SampleForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
