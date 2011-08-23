################################################## 
# UserListService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from UserListService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class UserListServiceLocator:
    UserListServiceInterface_address = "https://adwords.google.com:443/api/adwords/cm/v201008/UserListService"
    def getUserListServiceInterfaceAddress(self):
        return UserListServiceLocator.UserListServiceInterface_address
    def getUserListServiceInterface(self, url=None, **kw):
        return UserListServiceSoapBindingSOAP(url or UserListServiceLocator.UserListServiceInterface_address, **kw)

# Methods
class UserListServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getUserList
    def getUserList(self, request):
        if isinstance(request, getUserListRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getUserListResponse.typecode)
        return response

    # mutate: getUserList
    def mutateUserList(self, request):
        if isinstance(request, mutateUserListRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(mutateUserListResponse.typecode)
        return response

getUserListRequest = ns0.getUserList_Dec().pyclass

getUserListResponse = ns0.getUserListResponse_Dec().pyclass

mutateUserListRequest = ns0.mutateUserList_Dec().pyclass

mutateUserListResponse = ns0.mutateUserListResponse_Dec().pyclass