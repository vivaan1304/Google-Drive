from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=32)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=32)])
    password = PasswordField('Password', validators=[DataRequired()])
    rep_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match') ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        # print(user)
        if user is not None:
            print(user)
            raise ValidationError('Please Use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email-address')

class UploadForm(FlaskForm):
    file = MultipleFileField('Upload', validators=[FileRequired()])
    submit = SubmitField('Submit')


#, Email('please enter a valid email address')