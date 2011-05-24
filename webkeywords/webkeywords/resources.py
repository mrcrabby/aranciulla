from mongoalchemy.document import Document, Index, DocumentField
from mongoalchemy.fields import *
from pyramid.security import Allow, Everyone, Authenticated

class User(Document):
	email = StringField()
	password = StringField()
	max_keys = IntField()
	
	
class Root(object):
	__parent__ = None
	__name__ = ''
	__acl__ = [ (Allow, Authenticated, 'view'),
                (Allow, 'group:admin', 'admin') ]
                
	def __init__(self, request):
		self.request = request
        
	def __getitem__(self,key):
		if key == 'category':
			return Category()
		if key == 'parent':
			return ByParent()
		raise KeyError      	

class ByParent(object):
	__parent__= Root
	__name__ = 'parent'
	
	def __getitem__(self, key):
		i = InstantKeywordMongo(parent=key)
		i.__parent__= ByParent
		i.__name__= key
		return i
        
class Category(object):
	__parent__= Root
	__name__ = 'category'
	__acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
	
	categories = ['ambiente','tecnologia','auto_e_moto','bellezza_e_benessere','casa_e_decorazione',
	'cucina_e_alimentazione','cultura', 'economia_e_finanza','educazione_e_lavoro', 'moda_e_tendenza', 'sport'
	, 'svago_e_tempo_libero', 'tecnologia', 'viaggi']
		
	def __getitem__(self,key):
		if key in self.categories:
			return InstantKeywordMongo(category=key)

		
        
class InstantKeywordMongo(object):
 __parent__= None 
 __name__ = None
	
 def __init__(self, keyword=None, parent=None, category=None, level=None, dicts=None, depth=None, place=None, **kwargs):
  self.keyword = keyword
  self.parent = parent
  self.category = category
  self.level = level
  self.dicts = dicts
  self.depth = depth
  self.place = place
  self.has_child = False
  self.fields = ['keyword', 'level', 'dicts', 'depth', 'place', 'category', 'parent', 'has_child']
 
 def __str__(self):
  return '%s' % (self.keyword)
 
 def to_dict(self):
  d = dict()
  for field in self.fields:
  	value = getattr(self, field)
  	if value is not None and value is not False:
  		d[field] = value
  return d
