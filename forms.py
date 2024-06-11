from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired, Email, URL


class LoginForm(FlaskForm):
    user = EmailField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class RecentWork(FlaskForm):
    title = StringField(label='Work Title', validators=[DataRequired()])
    text_info = TextAreaField(label='Work Text', validators=[DataRequired()])
    img_url = StringField(label='Work Image URL', validators=[DataRequired(), URL()])
    work_url = StringField(label='Work URL', validators=[DataRequired(), ])
    submit = SubmitField(label='Save Work')


class PhotoProfile(FlaskForm):
    photo = FileField(label='Photo Profile', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'webp', 'jpeg', \
                                                                                      'svg', 'jfif'])])
    submit = SubmitField(label='Update Photo')


class Email(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Update Email')



