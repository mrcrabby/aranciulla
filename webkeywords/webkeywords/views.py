from pyramid.view import view_config
from pyramid.renderers import get_renderer
import re
from resources import *
from math import ceil
import pymongo
from mongoalchemy.session import Session
from pyramid.security import authenticated_userid, has_permission
	
def _get_user(request):
	email = authenticated_userid(request)
	with Session.connect(request.registry.settings['db_name'] ) as s:
		user = s.query(User).filter_by(email=email).one()
	return user

@view_config(name='pop', context='webkeywords.resources.Root', renderer='json')
def pop(context, request):
	with Session.connect(request.registry.settings['db_name'] ) as s:
		s.clear_collection(User)
		u = User(email='test1', password='test1', groups = ['admin'], scritti=[], bloccati=[])
		s.insert(u)
		return dict()

	

@view_config(name='admin', context='webkeywords.resources.Root', renderer='webkeywords:templates/admin.pt', permission='administer')
def admin(request):
	message = '' 
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
				user = User(email=login, password=password, max_keys=max_keys, groups=['admin'] if request.params.get('admin') else [],
							scritti = [],
							bloccati = [])
				s.insert(user)
				message = 'user created'
	
	return dict(message=message)

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
@view_config(context='webkeywords.resources.Root', renderer='webkeywords:templates/index.pt', permission='view')
@view_config(name='scritti', context='webkeywords.resources.Root', renderer='webkeywords:templates/index.pt', permission='view')
@view_config(name='bloccati', context='webkeywords.resources.Root', renderer='webkeywords:templates/index.pt', permission='view')
def search_keyword(context, request):
	k_mongo = InstantKeywordMongo()
	get_args = request.GET.copy()
	fields = list(k_mongo.fields)
	fields.remove('category')
	user = _get_user(request)	
	for field in fields:
		if field == 'keyword':
			k_mongo.keyword = re.compile(request.GET.get('keyword')) if request.GET.get('keyword') else None
		else:
			if request.GET.get(field):
				try:
					setattr(k_mongo, field, int(request.GET.get(field)))
				except:
					setattr(k_mongo, field, request.GET.get(field))
	
	if request.view_name == 'scritti' or request.view_name == 'bloccati':
		keys_to_get = getattr(user, request.view_name)
		if keys_to_get:
			filt = { '$or' : [dict(keyword=v) for v in  keys_to_get] }
		else:
			filt = None
	else:
		if user.scritti + user.bloccati:
			filt = {'$nor': [dict(keyword=v) for v in  user.scritti+user.bloccati]}
		else:
			filt = dict()
	
	inst_list = request.db.orderedkeys.find(dict(k_mongo.to_dict().items()+filt.items())) if filt is not None else []
	insts = [dict([(field, x.get(field)) for field in k_mongo.fields]) for x in inst_list]
	#crop keywords
	email = authenticated_userid(request)
	with Session.connect(request.registry.settings['db_name'] ) as s:
		user = s.query(User).filter_by(email=email).one()
		try:
			if user.max_keys > 0:
				insts = insts[:user.max_keys]
		except AttributeError:
			pass
	count = len(insts)
	cur_page = int(get_args.pop('page', 1))
	insts = insts[(cur_page-1)*items_per_page:cur_page*items_per_page]
	pages = int(ceil(count / items_per_page)+1) 
	more_pages = True if cur_page < pages else False
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
		
	if cur_page < pages:
		if cur_page + 3 >= pages:
			end_page = pages
		else:
			end_page = cur_page + 3
	else:
		end_page = 1
		
	for i in range(start_page, end_page+1):
		d = get_args.copy()
		d['page'] = i
		list_page_args.append(d)
	category_name = k_mongo.category.replace('_', ' ')	if k_mongo.category else None
	
	return {'total': count, 'more_pages':more_pages, 'category':k_mongo.category, 'category_name':category_name, 'keywords':insts, 'get_args':get_args,
	 'first_args':first_args, 'preview_args':preview_args, 'last_args':last_args, 'list_page_args':list_page_args,
	'end_args':end_args, 'cur_page': cur_page}

@view_config(name='scritto', context='webkeywords.resources.Root', renderer='json', permission='view')
@view_config(name='bloccato', context='webkeywords.resources.Root', renderer='json', permission='view')
def scritto(context, request):
	user = _get_user(request)
	keyword = request.GET.get('keyword')
	if request.view_name == 'scritto':
		attribute = 'scritti'
	else:
		attribute = 'bloccati'
	if keyword:
		try:
			getattr(user, attribute).append(keyword)
		except AttributeError:
			setattr(user, attribute, list())
			getattr(user, attribute).append(keyword)
	with Session.connect(request.registry.settings['db_name'] ) as s:
		s.insert(user)
	return dict(success=True)
	
@view_config(name='back', context='webkeywords.resources.Root', renderer='json', permission='view')
def back(context, request):
	user = _get_user(request)
	keyword = request.GET.get('keyword')
	try:
		user.scritti.remove(keyword)
		user.bloccati.remove(keyword)
	except ValueError:
		pass
	with Session.connect(request.registry.settings['db_name'] ) as s:
		s.insert(user)
	return dict()
