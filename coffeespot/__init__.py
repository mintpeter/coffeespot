from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import group_from_user

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
                          root_factory='coffeespot.models.RootFactory')
    config.include('pyramid_chameleon')
    authn_policy = AuthTktAuthenticationPolicy(
        settings['coffeespot.secret'], callback=group_from_user, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login/')
    config.add_route('logout', '/logout/')
    config.add_route('new_post', '/post/new/')
    config.add_route('edit_post', '/post/edit/{pid}/')
    config.add_route('view_post', '/post/view/{pid}/')
    config.scan()
    return config.make_wsgi_app()
