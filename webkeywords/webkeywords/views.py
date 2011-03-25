from pyramid.view import view_config
from pyramid.renderers import get_renderer
import re

def my_view(request):
    return {'content':'test'}

@view_config(name='search', context='webkeywords.resources.Root', renderer='webkeywords:templates/search.pt')
def search(context, request):
    base = get_renderer('templates/base.pt').implementation()
    return {'base': base}

@view_config(name='search', context='webkeywords.resources.Keyword', renderer='json')
def search_keyword(context, request):
    context.keyword = re.compile(request.GET.get('keyword')) if request.GET.get('keyword') else None
    context.depth = int(request.GET.get('depth')) if request.GET.get('depth') else None
    insts = [dict([('keyword', x.get('keyword')), ('depth', x.get('depth'))]) for x in request.db.keywords.find(context.to_dict())]
    return insts