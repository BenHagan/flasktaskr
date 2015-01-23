# forms.py

from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, \
    SelectField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Email

class AddTaskForm(Form):
    task_id = IntegerField('Priority')
    name = TextField('Task Name', validators=[InputRequired()])
    due_date = DateField(
        'Due Date (mm/dd/yyyy)',
        validators=[InputRequired()], format='%m/%d/%Y'
        )
    priority = SelectField(
        'Priority',
        validators=[InputRequired()],
        choices=[
            ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')
            ]
        )
    status = IntegerField('Status')

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