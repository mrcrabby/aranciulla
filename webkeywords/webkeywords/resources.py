class Root(object):
    def __init__(self, request):
        print 'root __init__'
        self.request = request
        
    def __getitem__(self,key):
        print 'getitem called'
        print 'key: ', key
        if key == 'keyword':
            print 'correct return'
            return Keyword()

        
class Keyword(object):
    def __init__(self, *args, **kwargs):
        self.keyword = kwargs.get('keyword')
        self.depth = kwargs.get('depth')
    
    def __str__(self):
        return '%s' % (self.keyword)
    
    def to_dict(self):
        d = dict()
        d['keyword'] = self.keyword
        d['depth'] = self.depth
        return d

        
        
def get_root(request):
    root = Root(request)
    root['Keyword'] = Keyword()
    return root