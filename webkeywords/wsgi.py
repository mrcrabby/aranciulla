from pyramid.paster import get_app

application = get_app(
  '/var/www/argomenti.in/aranciulla/webkeywords/production.ini', 'main')
