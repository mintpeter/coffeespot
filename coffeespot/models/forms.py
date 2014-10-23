from wtforms import (
    Form,
    BooleanField,
    HiddenField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField)
from wtforms.validators import Length, optional

from .tables import DBSession, Categories

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


categories = DBSession.query(Categories).order_by(Categories.name)
categories = [(c.id, c.name) for c in categories.all()]

class PostForm(Form):
    title = StringField('Title', [Length(min=1)])
    category = SelectField('Category', coerce=int, choices=categories)
    post_content = TextAreaField('Post', [Length(min=1)])
    submit = SubmitField('Submit Post')
