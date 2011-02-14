#!/usr/bin/python
# -*- coding: UTF-8 -*-


from xml.dom.minidom import parseString
from progressbar import ProgressBar
from xml.dom.minidom import Document
import urllib2
import sys


class KeywordEntry(Keyword):
    def __init__(self, keyword, key, match_type=None, global_score=None, regional_score=None):
        self.keyword = unicode(keyword)
        self.key = unicode(key)
        self.children = list()
        self.selected = False
        self.match_type = match_type
        self.global_score = global_score
        self.regional_score = regional_score
            
    def __str__(self):
        return 'keyword:%s    key:%s    match_type:%s    global:%s    regional:%s' % (self.keyword, self.key, self.match_type, self.global_score, self.regional_score)
    
    def __repr__(self):
        return self.__str__()

class Tree():
    def __init__(self, main):
        self.el = main
        self.next = list()


class KeywordManager():
    def __init__(self, keyword):
        self.stopwords = (u'ad', u'al', u'allo', u'ai', u'agli', u'all', u'agl', u'alla', u'alle', u'con', u'col', u'coi', u'da', u'dal', u'dallo', u'dai', u'dagli', u'dall', u'dagl', u'dalla', u'dalle', u'di', u'del', u'dello', u'dei', u'degli', u'dell', u'degl', u'della', u'delle', u'in', u'nel', u'nello', u'nei', u'negli', u'nell', u'negl', u'nella', u'nelle', u'su', u'sul', u'sullo', u'sui', u'sugli', u'sull', u'sugl', u'sulla', u'sulle', u'per', u'tra', u'contro', u'io', u'tu', u'lui', u'lei', u'noi', u'voi', u'loro', u'mio', u'mia', u'miei', u'mie', u'tuo', u'tua', u'tuoi', u'tue', u'suo', u'sua', u'suoi', u'sue', u'nostro', u'nostra', u'nostri', u'nostre', u'vostro', u'vostra', u'vostri', u'vostre', u'mi', u'ti', u'ci', u'vi', u'lo', u'la', u'li', u'le', u'gli', u'ne', u'il', u'un', u'uno', u'una', u'ma', u'ed', u'se', u'perché', u'anche', u'come', u'dov', u'dove', u'che', u'chi', u'cui', u'non', u'più', u'quale', u'quanto', u'quanti', u'quanta', u'quante', u'quello', u'quelli', u'quella', u'quelle', u'questo', u'questi', u'questa', u'queste', u'si', u'tutto', u'tutti', u'a', u'c', u'e', u'i', u'l', u'o', u'ho', u'hai', u'ha', u'abbiamo', u'avete', u'hanno', u'abbia', u'abbiate', u'abbiano', u'avrò', u'avrai', u'avrà', u'avremo', u'avrete', u'avranno', u'avrei', u'avresti', u'avrebbe', u'avremmo', u'avreste', u'avrebbero', u'avevo', u'avevi', u'aveva', u'avevamo', u'avevate', u'avevano', u'ebbi', u'avesti', u'ebbe', u'avemmo', u'aveste', u'ebbero', u'avessi', u'avesse', u'avessimo', u'avessero', u'avendo', u'avuto', u'avuta', u'avuti', u'avute', u'sono', u'sei', u'è', u'siamo', u'siete', u'sia', u'siate', u'siano', u'sarò', u'sarai', u'sarà', u'saremo', u'sarete', u'saranno', u'sarei', u'saresti', u'sarebbe', u'saremmo', u'sareste', u'sarebbero', u'ero', u'eri', u'era', u'eravamo', u'eravate', u'erano', u'fui', u'fosti', u'fu', u'fummo', u'foste', u'furono', u'fossi', u'fosse', u'fossimo', u'fossero', u'essendo', u'faccio', u'fai', u'facciamo', u'fanno', u'faccia', u'facciate', u'facciano', u'farò', u'farai', u'farà', u'faremo', u'farete', u'faranno', u'farei', u'faresti', u'farebbe', u'faremmo', u'fareste', u'farebbero', u'facevo', u'facevi', u'faceva', u'facevamo', u'facevate', u'facevano', u'feci', u'facesti', u'fece', u'facemmo', u'faceste', u'fecero', u'facessi', u'facesse', u'facessimo', u'facessero', u'facendo', u'sto', u'stai', u'sta', u'stiamo', u'stanno', u'stia', u'stiate', u'stiano', u'starò', u'starai', u'starà', u'staremo', u'starete', u'staranno', u'starei', u'staresti', u'starebbe', u'staremmo', u'stareste', u'starebbero', u'stavo', u'stavi', u'stava', u'stavamo', u'stavate', u'stavano', u'stetti', u'stesti', u'stette', u'stemmo', u'steste', u'stettero', u'stessi', u'stesse', u'stessimo', u'stessero', u'stando', u'far', u'piu', u'click', u'collegati', u'sito', u'Internet', u'file', u'pulsante', u'voce', u'finestra', u'avanti', u'fine', u'infine', u'apre', u'a questo punto', u'poi', u'barra', u'devi', u'puoi', u'avere', u'vuoi', u'se', u'fare', u'subito', u'clicca', u'pagina', u'uno', u'due', u'tre', u'dopo', u'essere', u'possono', u'tasto', u'mouse', u'destro', u'sinistro', u'appena', u'sempre', u'destra', u'sinistra', u'modulo', u'tutte', u'tutti', u'quindi', u'accanto', u'sotto', u'presente', u'collocato', u'collocata', u'ormai', u'molto', u'poco', u'for', u'in', u'per', u'is')
        self.bannedwords = set([u'ke', u'keygen', u'yhaoo', u'dounload', u'downlo', u'gartis', u'ome', u'adesso', u'grazie', u'ecco', u'forum', u'italino', u'licenza', u'descargar', u'gratuit', u'telecharger', u'7F5', u'win32', u'win 32', u'descargare', u'grati', u'trojandownloader', u'fastwebnet', u'scn', u'sondrio', u'mese', u'ilpc', u'vers', u'istalare', u'downloada', u'scansini', u'gratisyahoo', u'yahoo', u'answers', u'2004', u'0F49', u'warcraft', u'9F5', u'47Fc', u'9F5', u'cme', u'euro', u'crack', u'free', u'ita', u'seriale', u'donwoland', u'dowloand', u'cazzo', u'yahoo', u'answers', u'dowland', u'xke', u'nn', u'descarca', u'dawnload', u'2009', u'2010', u'2008', u'2007', u'scaricre', u'gradis', u'dowload', u'wnload', u'telecharge', u'donwload', u'itliano', u'gigi', u'porno', u'saks fifth ave link', u'prer', u'downloades', u'downloads', u'3F15', u'3F14', u'xnavigation', u'tuttogratis', u'tutto gratis', u'softonic', u'aranzulla', u'serial', u'full', u'inglis', u'scarecari', u'gratias', u'downloadf', u'dawload', u'architettura', u'arch', u'windw', u'serverfr', u'kadu', u'poret', u'migliorr', u'x', u'gta', u'sever', u'1F7F7', u'malavida', u'8F5', u'vogli', u'alpha', u'beta', u'porn', u'porno', u'sex', u'sexy', u'sesso', u'gay', u'lesbo', u'sotwer', u'donwold', u'softwere', u'pi', u'messanger', u'ultimaa', u'scaricanuova'])
        self.bannedchars = set([u'.', u',', u'\'', u'"'])
        self.keyword_entries = list()
        self.keyword = unicode(keyword, 'utf-8')
    
    def importKeywords(self,keyword, keywords):
        self.keywords = [unicode(k) for k in keywords]
        self.__gen_key_entries()
        
    def __gen_key_entries(self):
        for key in self.keywords:
            norm_key = self.__genKey(key)
            duplicate = False
            for entry in self.keyword_entries:
                if entry.key == norm_key:
                    duplicate = True
            if(not duplicate):
                self.keyword_entries.append(KeywordEntry(key, norm_key))
    
    def importStructuredKeywords(self,keyword, keywords_dict):
        self.keywords = [unicode(k.get('keyword')) for k in keywords_dict[4:]]
        self.__gen_key_entries()
        for entry in self.keyword_entries:
            for d in keywords_dict:
                if d.get('keyword') == entry.keyword:
                    entry.match_type = d.get('match_type')
                    entry.global_score = d.get('global_score')
                    entry.regional_score = d.get('regional_score')
                    break
        
    def getKeywords(self):
        return list(self.keywords)
    
    def getKeywordEntries(self):
        return list(self.keyword_entries)
        
    def filterBannedwords(self, content):
        return [keyword for keyword in content if all(word not in self.bannedwords for word in keyword.split())]

    def filterBannedchars(self):
        return [keyword for keyword in self.keywords if all(char not in keyword for char in self.bannedchars)]
        
    def genXml(self, lower_bound, upper_bound, url=None,  *args, **kwargs):        
        filter_done = set()
        filter_missed = set()
        
        filter = False
        if url:
            filter = True
        valid = True
        
        doc = Document()
        cat = doc.createElement("keyword")
        cat.setAttribute('key', self.keyword)
        doc.appendChild(cat)
        
        pbar = ProgressBar(maxval=len(self.keyword_entries)).start()
        entries = list()  
        for i,obj in enumerate(self.keyword_entries):
            pbar.update(i)
            if filter:
                if self.__retrieve_keyword_presence_in_page(url, obj.key, filter_done, filter_missed):
                    valid = True
                else:
                    valid = False
             
            if valid:
                entries.append(obj.keyword)
            
            if len(entries) >= upper_bound:
                break
            
        #Create the xml now
        for entry in entries:
            child = doc.createElement("entry")
            child.setAttribute("key", entry)
            cat.appendChild(child)
            
        pbar.finish()
        sys.stdout.write('\n')
        return doc


    def __genKey(self, generated_keyword):
        '''Per identificarle, basta eliminare le stopword e riordinare le parole delle keyword in modo tale da individuare quelle duplicate, che vanno rimosse.'''
        
        list = generated_keyword.split()
        
        popped = False
        #put keyword at top
        while True: 
            if self.keyword in list:
                list.pop(list.index(self.keyword))
                popped = True
            else:
                break
        
        #remove stopwords    
        for stopword in self.stopwords:
            if stopword in list:
                list.pop(list.index(stopword))
        
        list.sort()
        
        if popped:
            return ' '.join([self.keyword]+list)
        else:
            return ' '.join(list)
    
    def __relation(self, key1, key2):
        if key1 != key2:
            return all(word in key2.split() for word in key1.split())
        else:
            return False
        
    def __retrieve_keyword_presence_in_page(self, url, keyword, filter_done, filter_missed, *args, **kwargs):
        if any(word in filter_missed for word in keyword.split()):
            return False
        
        res = True
        
        words = [word for word in keyword.split() if word not in filter_done.union(filter_missed)]
        for word in words:
            try:
                page = urllib2.urlopen(url+word).read()
            except UnicodeEncodeError:
                continue
            if "Nessun articolo trovato. Vuoi provare una ricerca diversa?" in page:
                filter_missed.add(word)
                res = False
            else:
                filter_done.add(word)
        
        return res
    
    def sort(self, field='global_score'):
        self.keyword_entries.sort(key=lambda x: getattr(x, field), reverse=True)
    
    def get(self, l, m):
        return self.keyword_entries[l:m]
    
    def removeUncleanKeywords(self):
        self.keyword_entries = [k for k in self.keyword_entries if self.keyword in k.key]
    
    def removeEqualGlobalsAndRegionals(self):
        self.sort()
        self.keyword_entries = [v for k,v in dict(((x.global_score, x.regional_score), x) for x in self.keyword_entries[::-1]).iteritems() ]        
