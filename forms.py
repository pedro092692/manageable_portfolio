from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField, FileField, SelectField
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
    submit_photo = SubmitField(label='Update Photo')


class Email(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    submit_email = SubmitField(label='Update Email')


class GivenName(FlaskForm):
    name = StringField(label='Name info for contact')
    submit_name = SubmitField(label='Update Name')


class Bio(FlaskForm):
    bio = StringField(label='Bio Information Data', validators=[DataRequired()])
    submit_bio = SubmitField(label='Update Bio')


class SocialNetwork(FlaskForm):
    name = SelectField(label='Social Network Name', choices=[('linkedin', 'LinkedIn'), ('github', 'Github'),
                                                             ('facebook', 'Facebook'), ('pinterest', 'Pinterest'),
                                                             ('behance', 'Behance'), ('instagram', 'Instagram'),
                                                             ('twitter', 'Twitter'), ('youtube', 'Youtube'),
                                                             ('tiktok', 'Tiktok'), ('whatsapp', 'Whatsapp')],
                       validators=[DataRequired()])
    url = StringField(label='Url', validators=[DataRequired(), URL()])
    submit_social = SubmitField(label='Save Social Network')


class PageMainTitle(FlaskForm):
    title = StringField(label='Main Title Value', validators=[DataRequired()])
    submit_title = SubmitField('Update Title')


class MainText(FlaskForm):
    text = StringField(label='Page Main Text', validators=[DataRequired()])
    submit_text = SubmitField('Update Main Text')


class GetInTouch(FlaskForm):
    title = StringField(label='Get In Touch Title', validators=[DataRequired()])
    submit_get_in_touch_title = SubmitField('Update Get In Touch Title')


class GetInTouchText(FlaskForm):
    text = StringField(label='Get In Touch Text', validators=[DataRequired()])
    submit_get_in_touch_text = SubmitField('Update Get In Touch Text')


class UserForm(FlaskForm):
    user_email = EmailField(label='Email', validators=[DataRequired()])
    name = StringField(label='Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField('Create User')




