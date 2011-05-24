from pyramid.config import Configurator
from webkeywords.resources import Root
from pyramid.events import NewRequest, BeforeRender
from gridfs import GridFS
import pymongo
from mongoalchemy.session import Session
from milo_app import helpers
from pyramid.renderers import get_renderer

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	authn_policy = AuthTktAuthenticationPolicy(secret='webkeywordsSecretMessageForAuthToken')
	authz_policy = ACLAuthorizationPolicy()
	config = Configurator(root_factory=Root, settings=settings,
							authentication_policy=authn_policy,
							authorization_policy=authz_policy)
	db_uri = settings['db_uri']
	conn = pymongo.Connection(db_uri)
	config.registry.settings['db_conn'] = conn
	config.add_subscriber(add_mongo_db, NewRequest)
	config.add_subscriber(add_renderer_globals, BeforeRender)
	config.add_view('webkeywords.views.my_view',
                    context='webkeywords:resources.Root',
                    renderer='webkeywords:templates/index.pt',
                    permission='view')
	config.add_static_view('static', 'webkeywords:static')
	config.scan()
	return config.make_wsgi_app()

def add_mongo_db(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]
    event.request.db = db
    event.request.fs = GridFS(db)

def add_renderer_globals(event):
	event.update({'base': get_renderer('templates/base.pt').implementation()})
	event.update({'h': helpers})
