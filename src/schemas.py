from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Optional


class CreateNoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = TextAreaField('Category', validators=[Optional()])
    published = BooleanField('Published', validators=[Optional()])


class UpdateNoteForm(FlaskForm):
    title = StringField('Title', validators=[Optional(), Length(max=100)])
    content = TextAreaField('Content', validators=[Optional()])
    category = TextAreaField('Category', validators=[Optional()])
    published = BooleanField('Published', validators=[Optional()])
