from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SMTPSettingsForm(FlaskForm):
    smtp_server = StringField('SMTP Server', validators=[DataRequired()])
    smtp_port = StringField('SMTP Port', validators=[DataRequired()])
    smtp_username = StringField('SMTP Username', validators=[DataRequired()])
    smtp_password = PasswordField('SMTP Password', validators=[DataRequired()])
    submit = SubmitField('Save Settings')

class EmailForm(FlaskForm):
    recipient = StringField('Recipient', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    submit = SubmitField('Send Email')
