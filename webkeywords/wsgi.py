from pyramid.paster import get_app

application = get_app(
  'production.ini', 'main')