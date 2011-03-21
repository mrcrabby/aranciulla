from pyramid.view import view_config
from pyramid.renderers import get_renderer


def my_view(request):
    return {'content':'test'}

@view_config(name='search', context='webkeywords.resources.Root', renderer='webkeywords:templates/search.pt')
def search(context, request):
    base = get_renderer('templates/base.pt').implementation()
    return {'base': base}

@view_config(name='search', context='webkeywords.resources.Keyword', renderer='json')
def search_keyword(context, request):
    return {'keyword': context.keyword, 'depth': context.depth}