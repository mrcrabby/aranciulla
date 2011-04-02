from pyramid.config import Configurator
from webkeywords.resources import Root
from pyramid.events import NewRequest
from gridfs import GridFS
import pymongo

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    db_uri = settings['db_uri']
    conn = pymongo.Connection(db_uri)
    config.registry.settings['db_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)

    config.add_view('webkeywords.views.my_view',
                    context='webkeywords:resources.Root',
                    renderer='webkeywords:templates/index.pt')
    config.add_static_view('static', 'webkeywords:static')
    config.scan()
    return config.make_wsgi_app()

def add_mongo_db(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]
    event.request.db = db
    event.request.fs = GridFS(db)

