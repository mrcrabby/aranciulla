from pyramid.view import view_config
from pyramid.renderers import get_renderer
import re
from resources import *
from math import ceil
import pymongo
from mongoalchemy.session import Session

@view_config(name='admin', context='webkeywords.resources.Root', renderer='webkeywords:templates/admin.pt', permission='view')
def admin(request): 
	if 'form.submitted' in request.params:
		login = request.params['login']
		password = request.params['password']
		max_keys = request.params['max_keys']
		try:
			max_keys = int(max_keys)
		except:
			max_keys = -1
		with Session.connect(request.registry.settings['db_name'] ) as s:
			try:
				user = s.query(User).filter_by(email=login).one()
			except:
				user = User(email=login, password=password, max_keys=max_keys)
				s.insert(user)
	count = request.db.orderedkeys.find().count()
	return dict(max_keywords=count)

@view_config(name='logs-google',context='webkeywords.resources.Root', renderer='webkeywords:templates/logs.pt')
@view_config(name='logs',context='webkeywords.resources.Root', renderer='webkeywords:templates/logs.pt')
def show_logs(request):
	ufile = '/tmp/keygrabber.log'
	if request.view_name == 'logs-google':
		ufile = '/tmp/keygrabber-google.log'
	f = open(ufile)
	data = list()
	for line in f.readlines():
		try:
			data.append(unicode(line))
		except:
			pass
	return dict(filecontent=data)	

def my_view(request):
	c = InstantKeywordMongo()    
	return search_keyword(c, request)

items_per_page = 30
@view_config(context='webkeywords.resources.InstantKeywordMongo', renderer='webkeywords:templates/index.pt', permission='view')
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
	
	
	inst_list = request.db.orderedkeys.find(context.to_dict())
	insts = [dict([(field, x.get(field)) for field in context.fields]) for x in inst_list]
	count = len(insts)
	cur_page = int(get_args.pop('page', 1))
	insts = insts[(cur_page-1)*items_per_page:cur_page*items_per_page]
	pages = int(ceil(count / items_per_page)+1) 
	more_pages = True if cur_page+3 < pages else False
	first_args = get_args.copy()
	first_args['page'] = 1
	preview_args = get_args.copy()
	preview_args['page'] = max(cur_page - 1, 1)
	last_args = get_args.copy()
	last_args['page'] = pages
	end_args = get_args.copy()
	end_args['page'] = max(cur_page + 1, 1)
	list_page_args = list()
	if cur_page > 3:
		start_page = cur_page -3
	elif cur_page == 3:
		start_page = cur_page -2
	elif cur_page == 2:
		start_page = cur_page -1
	else:
		start_page = cur_page
	end_page = cur_page + 3
	for i in range(start_page, end_page+1):
		d = get_args.copy()
		d['page'] = i
		list_page_args.append(d)
	category_name = context.category.replace('_', ' ')	if context.category else None
	print(request.resource_url(context, query=get_args))	
	return {'total': count, 'more_pages':more_pages, 'category':context.category, 'category_name':category_name, 'keywords':insts, 'get_args':get_args,
	 'first_args':first_args, 'preview_args':preview_args, 'last_args':last_args, 'list_page_args':list_page_args,
	'end_args':end_args}
