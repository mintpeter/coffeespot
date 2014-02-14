#from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import (view_config,
                          forbidden_view_config,
                          notfound_view_config)
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember, forget, authenticated_userid

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Posts,
    Users
    )

from markupsafe import Markup

import transaction, markdown

from .security import verify_password

@view_config(route_name='home', renderer='home.mak')
def home(request):
    posts = DBSession.query(Posts).all()
    for post in posts:
        post.post = Markup(markdown.markdown(post.post))
    
    return {'posts': posts, 'username': authenticated_userid(request)}
    
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
                         post=post_content)
        with transaction.manager:
            DBSession.add(new_post)
        return {'message': 'Post successfully added.', 'post': post_content}
    else:
        return {'message': '',
                'post': '',
                'url': request.route_url('new_post')}

@view_config(route_name='edit_post', renderer='edit_post.mako',
             permission='edit')
def edit_post(request):
    post_id = request.matchdict['pid']
    post = DBSession.query(Posts).filter(Posts.id == post_id).first()
    if 'submitted' in request.params:
        post_title = request.params.get('title')
        post_content = request.params.get('post_content')
        changed = False
        if post_title != post.title:
            changed = True
            post.title = post_title
        if post_content != post.post:
            changed = True
            post.post = post_content
        if changed:
            with transaction.manager:
                DBSession.add(post)
        return HTTPFound(location=request.route_url('view_post', pid=post_id))
    else:
        return {'url': request.route_url('edit_post', pid=post_id),
                    'post': post}

@view_config(route_name='delete_post', renderer='delete_post.mako')
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
        return {'url': request.route_url('delete_post', pid=post_id),
                'post': post,
                'message': 'Are you sure you want to delete this post?'}

@view_config(route_name='view_post', renderer='view_post.mako')
def view_post(request):
    post_id = request.matchdict['pid']
    post = DBSession.query(Posts).filter(Posts.id == post_id).first()
    if post is None:
        message = 'The post you requested does not exist.'
    else:
        post.post = Markup(markdown.markdown(post.post))
        message = False
    return {'message': message, 'post': post}

@notfound_view_config(append_slash=True, renderer='404.mako')
def notfound(request):
    return {}
