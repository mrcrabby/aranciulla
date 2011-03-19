class Root(object):
    __parent__=None
    __name__=None
    def __init__(self, request):
        self.request = request
