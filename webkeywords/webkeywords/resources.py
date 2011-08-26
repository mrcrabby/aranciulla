from mongoalchemy.document import Document, Index, DocumentField
from mongoalchemy.fields import *
from pyramid.security import Allow, Everyone, Authenticated
from mongoalchemy.session import Session

#admin user
#{"max_keys" : -1, "password" : "test1", "email" : "test1", "groups" : [ "admin" ] }
#> db.User.save({"password" : "test1", "email" : "test1", "groups" : [ "admin" ], scritti: [], bloccati: [] })
class User(Document):
	email = StringField()
	password = StringField()
	max_keys = IntField(required=False)
	groups = ListField(StringField(), required=False)
	scritti = ListField(StringField(), required=False)
	bloccati = ListField(StringField(), required=False)
	
	def __str__(self):
		return '%s %s %s' % (self.email, self.password, self.groups)	
		
def groupfinder(userid, request):
	with Session.connect(request.registry.settings['db_name'] ) as s:
		user = s.query(User).filter_by(email=userid).one()
	try:
		r = user.groups
	except AttributeError:
		r = []
	return r

	
class Root(object):
	__parent__ = None
	__name__ = ''
	__acl__ = [ (Allow, Authenticated, 'view'),
                (Allow, 'admin', 'administer') ]
	def __init__(self, request):
		self.request = request
        
	def __getitem__(self,key):
		if key == 'category':
			c = Category(self.request)
			c.__parent__ = self
			return c
		if key == 'parent':
			p = ByParent()
			p.__parent__= self
			return p
		raise KeyError      	

class ByParent(object):
	__parent__= Root
	__name__ = 'parent'
	
	def __getitem__(self, key):
		i = InstantKeywordMongo(parent=key)
		i.__parent__= self 
		return i
        
class Category(object):
	__parent__= Root
	__name__ = 'category'
	
	def __init__(self, request):
		self.request = request
		self.categories = self.request.db.orderedkeys.distinct('category')
		
	def __getitem__(self,key):
		if key in self.categories:
			i = InstantKeywordMongo(category=key)
			i.__parent__= self 
			return i

class InstantKeywordMongo(object):
	__parent__= None 
	__name__ = None
    
	def __init__(self, keyword=None, parent=None, category=None, level=None, dicts=None, depth=None, place=None, dbplace=None, **kwargs):
		self.keyword = keyword
		self.parent = parent
		self.category = category
		self.level = level
		self.dicts = dicts
		self.depth = depth
		self.place = place
		self.dbplace = dbplace
		self.has_child = False
		self._id = None
		self.global_searches = None
		self.regional_searches = None
		self.fields = ['keyword', 'level', 'dicts', 'depth', 'place', 'dbplace', 'category', 'parent', 'has_child', '_id', 'global_searches', 'regional_searches']
	def __str__(self):
		return 'keyword: %s, parent: %s, dicts: %s, level: %s, depth: %s, dbplace: %s, place: %s' % (self.keyword, self.parent, self.dicts, self.level, self.depth, self.dbplace, self.place)

	def to_dict(self):
		d = dict()
		for field in self.fields:
			value = getattr(self, field)
			if value is not None and value is not False:
				d[field] = value
		return d
