#from pyramid.response import Response
from pyramid.view import (view_config,
                          forbidden_view_config,
                          notfound_view_config)
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember, forget, authenticated_userid
from pyramid.events import subscriber, BeforeRender

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Posts,
    Users,
    Categories
    )

from markupsafe import Markup

import transaction, markdown

from .security import verify_password

@subscriber(BeforeRender)
def add_globals(event):
    event['userid'] = authenticated_userid(event['request'])

@view_config(route_name='home', renderer='home.mako')
def home(request):
    posts = DBSession.query(Posts, Users, Categories)
    posts = posts.filter(Posts.authorid == Users.id)
    posts = posts.filter(Posts.categoryid == Categories.id)
    posts = posts.order_by(Posts.id.desc()).all()
    
    return {'posts': posts}
    
#    try:
#        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#    except DBAPIError:
#        return Response(conn_err_msg, content_type='text/plain', status_int=500)
#    return {'one': one, 'project': 'coffeespot'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_coffeespot_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


@view_config(route_name='login', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if login_url == referrer:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    if 'submitted' in request.params:
        username = request.params.get('username')
        password = request.params.get('password')
        if verify_password(username, password):
            headers = remember(request, username)
            return HTTPFound(location=came_from, headers=headers)
        else:
            message = 'Incorrect login information.'
            return {'message': message,
                    'username': username,
                    'came_from': came_from,
                    'url': request.route_url('login')
                    }
    else:
        return {'message': '',
                'username': '',
                'came_from': came_from,
                'url': request.route_url('login')
                }

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)

@view_config(route_name='new_post', renderer='new_post.mako',
             permission='edit')
def new_post(request):
    if 'submitted' in request.params:
        title = request.params.get('title')
        users_db = DBSession.query(Users)
        author = users_db.filter(Users.name == authenticated_userid(request))
        post_content = request.params.get('post_content')
        new_post = Posts(title=title,
                         authorid=author.first().id,
                         categoryid=1,
                         post=post_content)
        with transaction.manager:
            DBSession.add(new_post)
        return {'message': 'Post successfully added.', 'post': post_content}
    else:
        categories = DBSession.query(Categories).order_by(Categories.name)
        categories = categories.all()
        return {'message': '',
                'post': '',
                'categories': categories,
                'url': request.route_url('new_post')}

@view_config(route_name='edit_post', renderer='edit_post.mako',
             permission='edit')
def edit_post(request):
    post_id = request.matchdict['pid']
    post = DBSession.query(Posts).filter(Posts.id == post_id).first()
    if 'submitted' in request.params:
        post_title = request.params.get('title')
        post_category = request.params.get('category')
        post_content = request.params.get('post_content')
        changed = False
        if post_title != post.title:
            changed = True
            post.title = post_title
        if post_content != post.post:
            changed = True
            post.post = post_content
        if post_category != post.categoryid:
            changed = True
            post.categoryid = post_category
        if changed:
            with transaction.manager:
                DBSession.add(post)
        return HTTPFound(location=request.route_url('view_post', pid=post_id))
    else:
        categories = DBSession.query(Categories).order_by(Categories.name)
        categories = categories.all()
        return {'url': request.route_url('edit_post', pid=post_id),
                'categories': categories,
                'post': post}

@view_config(route_name='delete_post', renderer='delete_post.mako',
             permission='edit')
def delete_post(request):
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
    post_id = request.matchdict['pid']
    post = DBSession.query(Posts).filter(Posts.id == post_id).first()
    if post is None:
        message = 'The post you requested does not exist.'
    else:
        message = False
    return {'message': message, 'post': post}

@view_config(route_name='new_category', renderer='new_category.mako',
             permission='edit')
def new_category(request):
    if 'submitted' in request.params:
        category_name = request.params.get('category_name')
        new_category = Categories(category_name)
        with transaction.manager:
            DBSession.add(new_category)
        return HTTPFound(location=request.route_url('home'))
    else:
        return {'url': request.route_url('new_category')}

@view_config(route_name='edit_category', renderer='edit_category.mako',
             permission='edit')
def edit_category(request):
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

@view_config(route_name='view_category', renderer='home.mako')
def view_category(request):
    category_id = request.matchdict['cid']
    posts = DBSession.query(Posts, Users, Categories)
    posts = posts.filter(Posts.categoryid == category_id)
    posts = posts.filter(Posts.authorid == Users.id)
    posts = posts.filter(Posts.categoryid == Categories.id)
    posts = posts.order_by(Posts.id.desc()).all()
    return {'posts': posts}

@notfound_view_config(append_slash=True, renderer='404.mako')
def notfound(request):
    return {}
