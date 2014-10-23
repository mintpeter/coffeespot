from wtforms import (
    Form,
    BooleanField,
    HiddenField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField)
from wtforms.validators import Length, optional

groups = [(1, 'editor'), (0, 'admin')]

class UserForm(Form):
    name = StringField('Username', [Length(min=2, max=15)])
    password = PasswordField('Password', [Length(min=6)])
    group = SelectField('Group', coerce=int, choices=groups)
    submit = SubmitField('Submit')

class EditUserForm(UserForm):
    delete = BooleanField('Delete')
    password = PasswordField('Password', [optional(), Length(min=6)])
    user_id = HiddenField()
    group = HiddenField()

class LoginForm(Form):
    came_from = HiddenField()
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')
