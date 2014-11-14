from pyramid import config as c
from pyramid.view import (view_config,
                          forbidden_view_config,
                          notfound_view_config)
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden,
    HTTPNotFound,
    HTTPUnauthorized
    )
from pyramid.security import remember, forget, authenticated_userid
from pyramid.events import subscriber, BeforeRender

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound
import transaction

import markdown
from wtforms import Form

from passlib.hash import bcrypt

from models.tables import (
    DBSession,
    Posts,
    Users,
    Categories
    )

from models.forms import (
    LoginForm, 
    UserForm, 
    EditUserForm, 
    PostForm,
    CategoryForm
    )

from .security import verify_password

@subscriber(BeforeRender)
def add_globals(event):
    """Store the username in the application registry. This should probably use
    a session instead.
    """

    username = authenticated_userid(event['request'])
    if username:
        c.user = DBSession.query(Users)\
                    .filter(Users.name == username).first()
    else:
        c.user = None
    event['c'] = c


# This could be a generalized page-viewer. This would probably entail moving
# some Python to the template, which is kind of icky. I'll have to play with
# this.
@view_config(route_name='home', renderer='home.mako')
def home(request):
    """Get the posts for /home."""

    posts = DBSession.query(Posts, Users, Categories)\
                .join(Users, Posts.authorid==Users.id)\
                .join(Categories, Posts.categoryid==Categories.id)
    posts = posts.order_by(Posts.id.desc()).all()
    
    return {'posts': posts}

@view_config(route_name='login', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login(request):
    """If the user came from this page and has submitted the form, try to log
    them in. Otherwise, give them the login page.
    """

    login_url = request.route_url('login')
    referrer = request.url
    if login_url == referrer:
        referrer = '/'

    form = LoginForm(request.POST)
    if form.came_from.data:
        came_from = form.came_from.data
    else:
        came_from = referrer

    if request.POST and form.validate():
        username = form.username.data
        password = form.password.data
        if verify_password(username, password):
            headers = remember(request, username)
            return HTTPFound(location=came_from, headers=headers)
        else:
            message = 'Incorrect login information.'
            return {'message': message,
                    'username': username,
                    'form': form,
                    'came_from': came_from,
                    'url': request.route_url('login')
                    }
    else:
        return {'message': '',
                'username': '',
                'form': form,
                'came_from': came_from,
                'url': request.route_url('login')
                }

@view_config(route_name='logout')
def logout(request):
    """View for /logout, which ends the user's session."""

    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)

@view_config(route_name='new_post', renderer='new_post.mako',
             permission='edit')
def new_post(request):
    """View for /post/new. If the post has already been submitted, try to add it
    to the database and display a success message. Otherwise, show the new post
    form.
    """

    form = PostForm(request.POST)
    post_content = None
    if request.POST and form.validate():
        title = form.title.data
        category = form.category.data
        post_content = form.post_content.data
        
        users_db = DBSession.query(Users)
        author = users_db.filter(Users.name == authenticated_userid(request))
        
        new_post = Posts(title=title,
                         authorid=author.first().id,
                         categoryid=category,
                         post=post_content)
        
        with transaction.manager:
            DBSession.add(new_post)
        
    return {'form': form, 
            'post': post_content} #this should be run through markdown renderer

@view_config(route_name='edit_post', renderer='edit_post.mako',
             permission='edit')
def edit_post(request):
    """View for /post/edit. If the form's already been submitted, change it in
    the database. Otherwise, show the edit post form.
    """

    form = PostForm(request.POST)
    post_id = request.matchdict['pid']
    post = DBSession.query(Posts).filter(Posts.id == post_id).first()
    if request.POST and form.validate():
        title = form.title.data
        category = form.category.data
        content = form.category.content
        post.title = title
        post.post = content
        post.categoryid = category
        with transaction.manager:
            DBSession.add(post)
        return HTTPFound(location=request.route_url('view_post', pid=post_id))
    else:
        categories = DBSession.query(Categories).order_by(Categories.name)
        categories = categories.all()
        return {'form': form,
                'categories': categories,
                'post': post}

### wtforms probably wouldn't hurt here either.
@view_config(route_name='delete_post', renderer='delete_post.mako',
             permission='edit')
def delete_post(request):
    """View for /post/delete. If the user has already confirmed that they want
    to delete the post, delete it. Otherwise, ask them if they're sure.
    """

    post_id = request.matchdict['pid']
    post = DBSession.query(Posts).filter(Posts.id == post_id).first()
    if 'submitted' in request.params:
        with transaction.manager:
            DBSession.delete(post)
        return {'url': request.route_url('home'),
                'post': None,
                'message': 'Post successfully deleted.'}
    else:
        if 'no_delete' in request.params:
            url = request.route_url('home')
            post = None
            message = 'The post was not deleted.'
        else:
            url = request.route_url('delete_post', pid=post_id)
            message = 'Are you sure you want to delete this post?'
        return {'url': url,
                'post': post,
                'message': message}

@view_config(route_name='view_post', renderer='view_post.mako')
def view_post(request):
    """View for /post/view. Display a single post, with its comments thread."""

    post_id = request.matchdict['pid']
    post = DBSession.query(Posts).filter(Posts.id == post_id).one()
    if post is None:
        message = 'The post you requested does not exist.'
    else:
        message = False
    return {'message': message, 'post': post}

@view_config(route_name='new_category', renderer='new_category.mako',
             permission='admin')
def new_category(request):
    """View for /category/new. Adds a category."""

    form = CategoryForm(request.POST)
    if request.POST and form.validate():
        name = form.name.data
        new_category = Categories(name)
        with transaction.manager:
            DBSession.add(new_category)
        return HTTPFound(location=request.route_url('home'))
    else:
        return {'form': form}

### TODO: move to wtforms.
@view_config(route_name='edit_category', renderer='edit_category.mako',
             permission='admin')
def edit_category(request):
    """View for /category/edit. Edit or delete a category."""

    category_id = request.matchdict['cid']
    category = DBSession.query(Categories).filter(\
        Categories.id == category_id).first()
    if 'submitted' in request.params:
        if 'delete_category' in request.params:
            with transaction.manager:
                DBSession.remove(category)
        else:
            category.name = request.params.get('category_name')
            with transaction.manager:
                DBSession.add(category)
        return HTTPFound(location=request.route_url('home'))
    else:
        return {'url': request.route_url('edit_category', cid=category_id),
                'category': category}

# When there are no posts in the category, this page just tells you so. I think
# it would be sensible to offer to delete the category. This would suggest some
# kind of utility function, because it would duplicate some functionality in
# edit_category.
@view_config(route_name='view_category', renderer='home.mako')
def view_category(request):
    """View for /category/view. Display the posts in a single category."""

    category_id = request.matchdict['cid']
    posts = DBSession.query(Posts, Users, Categories)
    posts = posts.filter(Posts.categoryid == category_id)
    posts = posts.filter(Posts.authorid == Users.id)
    posts = posts.filter(Posts.categoryid == Categories.id)
    posts = posts.order_by(Posts.id.desc()).all()
    return {'posts': posts}

@view_config(route_name='new_user', renderer='new_user.mako', permission='admin')
def new_user(request):
    """View for /user/new. Add a new user!"""

    form = UserForm(request.POST)
    if request.POST and form.validate():
        password = bcrypt.encrypt(form.password.data)
        user = Users(form.name.data, form.group.data, password)
        DBSession.add(user)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}

@view_config(route_name='edit_user', renderer='edit_user.mako',
    permission='edit')
def edit_user(request):
    """View for /user/edit. Edit a user's attributes."""

    active_user = DBSession.query(Users)\
                    .filter(Users.name == authenticated_userid(request)).one()
    user_id = request.matchdict['uid']
    try:
        user = DBSession.query(Users).filter(Users.id == user_id).one()
    except NoResultFound:
        raise HTTPNotFound()
    if active_user.group != 0 and active_user is not user:
        raise HTTPUnauthorized()
    form = EditUserForm(request.POST)
    if request.POST and form.validate():
        if not form.delete.data:
            password = bcrypt.encrypt(form.password.data)
            user.name = form.name.data
            user.password = password
            DBSession.add(user)
            return HTTPFound(location=request.route_url('view_user', uid=user.id))
        else:
            DBSession.delete(user)
            return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'user': user}

# Since this is a blog, this should probably list their posts.
@view_config(route_name='view_user', renderer='view_user.mako')
def view_user(request):
    """View for /user/view. Look at a user's profile."""

    user_id = request.matchdict['uid']
    try:
        user = DBSession.query(Users)\
                .filter(Users.id == user_id)\
                .one()
        posts = DBSession.query(Posts)\
                .filter(Posts.authorid == user_id)\
                .all()
    except:
        raise HTTPNotFound()
        
    return {'user': user, 'posts': posts}

@view_config(context=HTTPUnauthorized, renderer='401.mako')
def unauthorized(request):
    """View for a 401 error. This is mostly for unauthenticated users, but it
    also gets called when somebody doesn't have rights to do something. See
    edit_user. That may not be the best way to do it, though.
    """

    return {}

@notfound_view_config(append_slash=True, renderer='404.mako')
def notfound(request):
    """View for a 404 error."""

    return {}
