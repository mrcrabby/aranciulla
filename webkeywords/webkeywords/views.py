from pyramid.view import view_config
from pyramid.renderers import get_renderer
import re
import resources
from math import ceil

@view_config(name='logs',context='webkeywords.resources.Root', renderer='webkeywords:templates/logs.pt')
def show_logs(request):
	f = open('/tmp/keygrabber.log')
	data = list()
	for line in f.readlines():
		try:
			data.append(unicode(line))
		except:
			pass
	return dict(filecontent=data)
	

def my_view(request):
	print('passing here')
	c = resources.InstantKeywordMongo()    
	return search_keyword(c, request)

items_per_page = 30
@view_config(context='webkeywords.resources.InstantKeywordMongo', renderer='webkeywords:templates/index.pt')
def search_keyword(context, request):
	get_args = request.GET.copy()
	fields = list(context.fields)
	fields.remove('category')	
	for field in fields:
		if field == 'keyword':
			context.keyword = re.compile(request.GET.get('keyword')) if request.GET.get('keyword') else None
		else:
			if request.GET.get(field):
				setattr(context, field, int(request.GET.get(field)))
	insts = [dict([(field, x.get(field)) for field in context.fields]) for x in request.db.keywords.find(context.to_dict())]
	count = len(insts)
	cur_page = int(get_args.pop('page', 1))
	insts = insts[(cur_page-1)*items_per_page:cur_page*items_per_page]
	pages = int(ceil(count / items_per_page)+1) 
	more_pages = True if cur_page+9 < pages else False
	end_page = min(cur_page+9, pages)
	first_args = get_args.copy()
	first_args['page'] = 1
	preview_args = get_args.copy()
	preview_args['page'] = max(cur_page - 1, 1)
	last_args = get_args.copy()
	last_args['page'] = pages
	end_args = get_args.copy()
	end_args['page'] = max(cur_page + 1, 1)
	list_page_args = list()
	for i in range(cur_page, end_page+1):
		d = get_args.copy()
		d['page'] = i
		list_page_args.append(d)
	category_name = context.category.replace('_', ' ')	if context.category else None
	print(request.resource_url(context, query=get_args))	
	return {'total': count, 'more_pages':more_pages, 'category':context.category, 'category_name':category_name, 'keywords':insts, 'get_args':get_args,
	 'first_args':first_args, 'preview_args':preview_args, 'last_args':last_args, 'list_page_args':list_page_args,
	'end_args':end_args}
