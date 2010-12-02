################################################## 
# AdGroupService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from AdGroupService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class AdGroupServiceLocator:
    AdGroupServiceInterface_address = "https://adwords.google.com:443/api/adwords/cm/v200909/AdGroupService"
    def getAdGroupServiceInterfaceAddress(self):
        return AdGroupServiceLocator.AdGroupServiceInterface_address
    def getAdGroupServiceInterface(self, url=None, **kw):
        return AdGroupServiceSoapBindingSOAP(url or AdGroupServiceLocator.AdGroupServiceInterface_address, **kw)

# Methods
class AdGroupServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getAdGroup
    def getAdGroup(self, request):
        if isinstance(request, getAdGroupRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAdGroupResponse.typecode)
        return response

    # mutate: getAdGroup
    def mutateAdGroup(self, request):
        if isinstance(request, mutateAdGroupRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(mutateAdGroupResponse.typecode)
        return response

getAdGroupRequest = ns0.getAdGroup_Dec().pyclass

getAdGroupResponse = ns0.getAdGroupResponse_Dec().pyclass

mutateAdGroupRequest = ns0.mutateAdGroup_Dec().pyclass

mutateAdGroupResponse = ns0.mutateAdGroupResponse_Dec().pyclass
