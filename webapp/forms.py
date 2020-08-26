# Forms

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length

from database import User


class ChatForm(FlaskForm):
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=1)])
    send = SubmitField("Send")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=30)])
    login = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=30)])
    confirm = PasswordField(
        "Repeat Password", validators=[DataRequired(),
        EqualTo("password", message='Passwords must match.')])
    register = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError("Please use another username.")
