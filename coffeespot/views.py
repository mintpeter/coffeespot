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

import transaction

from .security import verify_password

@view_config(route_name='home', renderer='home.mako')
def home(request):
    posts = DBSession.query(Posts).all()
    
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
    if 'submitted' in request.params:
        post_id = request.params('post_id')
        post_title = request.params('post_title')
        post_content = request.params('post_content')
        post = DBSession.query(Posts).filter(Posts.id == post_id).first()
        message = ''
        if post_title != post.title:
            post.title = post_title
            message = 'Changes successfully written.'
        if post_content != post.content:
            post.content = post_content
            message = 'Changes successfully written.'
        if message != '':
            with transaction.manager:
                DBSession.add(post)
        else:
            message = 'You didn\'t change anything!'
        return {'message': message}
    else:
        post_id = request.matchdict['post_id']
        return {'post_id', post_id}

@notfound_view_config(append_slash=True, renderer='404.mako')
def notfound(request):
    return {}
