################################################## 
# AdExtensionOverrideService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from AdExtensionOverrideService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class AdExtensionOverrideServiceLocator:
    AdExtensionOverrideServiceInterface_address = "https://adwords.google.com:443/api/adwords/cm/v200909/AdExtensionOverrideService"
    def getAdExtensionOverrideServiceInterfaceAddress(self):
        return AdExtensionOverrideServiceLocator.AdExtensionOverrideServiceInterface_address
    def getAdExtensionOverrideServiceInterface(self, url=None, **kw):
        return AdExtensionOverrideServiceSoapBindingSOAP(url or AdExtensionOverrideServiceLocator.AdExtensionOverrideServiceInterface_address, **kw)

# Methods
class AdExtensionOverrideServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getAdExtensionOverride
    def getAdExtensionOverride(self, request):
        if isinstance(request, getAdExtensionOverrideRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAdExtensionOverrideResponse.typecode)
        return response

    # mutate: getAdExtensionOverride
    def mutateAdExtensionOverride(self, request):
        if isinstance(request, mutateAdExtensionOverrideRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(mutateAdExtensionOverrideResponse.typecode)
        return response

getAdExtensionOverrideRequest = ns0.getAdExtensionOverride_Dec().pyclass

getAdExtensionOverrideResponse = ns0.getAdExtensionOverrideResponse_Dec().pyclass

mutateAdExtensionOverrideRequest = ns0.mutateAdExtensionOverride_Dec().pyclass

mutateAdExtensionOverrideResponse = ns0.mutateAdExtensionOverrideResponse_Dec().pyclass
