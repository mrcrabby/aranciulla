# -*- coding: UTF-8 -*-
from adwords import keyword_adwords as kad
import pymongo
import logging


log = logging.getLogger('ordering')
log.addHandler(logging.FileHandler('/tmp/keygrabber-ordering.log', 'w'))

connection = pymongo.Connection()
DB = connection.webkeywords
CL_IN = DB.crawlerCopy
CL_OUT = DB.orderedkeys

def create_ordered_collection(inst_list):
	'''
	Create the CL_OUT collection adding an index element
	'''
		#add index
		log.info('adding index')
		for i, key in enumerate(inst_list):
			key['index']=i 
		#save to orderedkeys collection
		CL_OUT.drop()
		log.info('adding ordered keys :'+str(len(inst_list)))
		a = CL_OUT.insert(inst_list)
		CL_OUT.ensure_index('index')
		log.info('collection created successfully')
		return inst_list

def get_adwords_data(self, limit = 0):	
	'''
	Get adwords data and save it
	'''
	for item in CL_IN.find().limit(limit):
		d = kad.get_keyword_info(item.get('keyword'))
		item['global_searches'] = d.get('global_searches')
		item['regional_searches'] = d.get('regional_searches')
		CL_IN.save(item)
	
def order_by_adwords_data(keys):
	keys.sort(key=lambda x: x['global_searches'] if 'global_searches' in x and x['global_searches'] is not None else 0 , reverse=True)

def adwords_ordering(limit = 0):
	'''
	Il nuovo algoritmo di
	ordinamento funziona così: si fa query a Google per ogni keyword per
	recuperare traffico e CPC. Si crea un index ordinando i titoli da
	quelli che fanno più traffico a quelli che fanno meno traffico usando
	il traffico globale. I figli sono dati dai titoli che iniziano col
	titolo padre se i titoli figli fanno meno traffico del titolo padre
	(es: come scaricare musica è figlio di come scaricare se, ad esempio,
	come scaricare musica fa 100 ricerche al mese e come scaricare ne fa
	10000)
	'''
	keys = list()
	#get_adwords_data(limit)
	for item in CL_IN.find().limit(limit):
		keys.append(item)
	ordered_keys = order_by_adwords_data(keys)
	create_ordered_collection(ordered_keys)
		

if __name__ == "__main__":
	adwords_ordering(20000)
