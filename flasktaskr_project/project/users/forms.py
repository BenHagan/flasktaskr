# forms.py

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Email

class RegisterForm(Form):
    name = TextField(
        'Username',
        validators=[InputRequired(), Length(min=6, max=25)]
        )
    email = TextField(
        'Email',
        validators=[InputRequired(),
        Email(),
        Length(min=6, max=40)]
        )
    password = PasswordField(
        'Password',
        validators=[InputRequired(),
        Length(min=6, max=40)])
    confirm = PasswordField(
        'Repeat Password',
        [InputRequired(),
        EqualTo('password',
        message='Passwords must match')]
        )

class LoginForm(Form):
    name = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])