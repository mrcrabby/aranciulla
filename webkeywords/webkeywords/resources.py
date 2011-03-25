class Root(object):
    def __init__(self, request):
        self.request = request
        
    def __getitem__(self,key):
        if key == 'keyword':
            return Keyword()

        
class Keyword(object):
    def __init__(self, *args, **kwargs):
        self.keyword = kwargs.get('keyword')
        self.depth = kwargs.get('depth')
    
    def __str__(self):
        return '%s' % (self.keyword)
    
    def to_dict(self):
        d = dict()
        if self.keyword is not None:
            d['keyword'] = self.keyword
        if self.depth is not None:
            d['depth'] = self.depth
        return d
