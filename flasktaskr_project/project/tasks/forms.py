# forms.py

from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, \
    SelectField
from wtforms.validators import InputRequired

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