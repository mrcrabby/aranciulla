from pyramid.config import Configurator
from webkeywords.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('webkeywords.views.my_view',
                    context='webkeywords:resources.Root',
                    renderer='webkeywords:templates/base.pt')
    config.add_static_view('static', 'webkeywords:static')
    config.scan('webkeywords')
    return config.make_wsgi_app()

