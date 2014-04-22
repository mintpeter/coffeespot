from wtforms import (
    Form,
    StringField,
    PasswordField,
    SelectField,
    HiddenField,
    SubmitField)
from wtforms.validators import Length

groups = [(1, 'editor'), (0, 'admin')]

class UserForm(Form):
    name = StringField('Username', [Length(min=2, max=15)])
    password = PasswordField('Password', [Length(min=6)])
    group = SelectField('Group', coerce=int, choices=groups)
    submit = SubmitField('Login')

class EditUserForm(UserForm):
    user_id = HiddenField()
    group = HiddenField()
