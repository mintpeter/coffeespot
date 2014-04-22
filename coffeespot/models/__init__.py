from pyramid.security import Allow, Everyone

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 0, 'admin'),
                (Allow, 0, 'edit'),
                (Allow, 1, 'edit')]
    def __init__(self, request):
        pass
