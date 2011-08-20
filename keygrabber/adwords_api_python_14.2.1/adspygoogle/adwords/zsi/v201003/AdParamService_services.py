################################################## 
# AdParamService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from AdParamService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class AdParamServiceLocator:
    AdParamServiceInterface_address = "https://adwords.google.com:443/api/adwords/cm/v201003/AdParamService"
    def getAdParamServiceInterfaceAddress(self):
        return AdParamServiceLocator.AdParamServiceInterface_address
    def getAdParamServiceInterface(self, url=None, **kw):
        return AdParamServiceSoapBindingSOAP(url or AdParamServiceLocator.AdParamServiceInterface_address, **kw)

# Methods
class AdParamServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getAdParam
    def getAdParam(self, request):
        if isinstance(request, getAdParamRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAdParamResponse.typecode)
        return response

    # mutate: getAdParam
    def mutateAdParam(self, request):
        if isinstance(request, mutateAdParamRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(mutateAdParamResponse.typecode)
        return response

getAdParamRequest = ns0.getAdParam_Dec().pyclass

getAdParamResponse = ns0.getAdParamResponse_Dec().pyclass

mutateAdParamRequest = ns0.mutateAdParam_Dec().pyclass

mutateAdParamResponse = ns0.mutateAdParamResponse_Dec().pyclass
