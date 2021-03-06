################################################## 
# BidLandscapeService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from BidLandscapeService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class BidLandscapeServiceLocator:
    BidLandscapeServiceInterface_address = "https://adwords.google.com:443/api/adwords/cm/v201003/BidLandscapeService"
    def getBidLandscapeServiceInterfaceAddress(self):
        return BidLandscapeServiceLocator.BidLandscapeServiceInterface_address
    def getBidLandscapeServiceInterface(self, url=None, **kw):
        return BidLandscapeServiceSoapBindingSOAP(url or BidLandscapeServiceLocator.BidLandscapeServiceInterface_address, **kw)

# Methods
class BidLandscapeServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getBidLandscape
    def getBidLandscape(self, request):
        if isinstance(request, getBidLandscapeRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getBidLandscapeResponse.typecode)
        return response

getBidLandscapeRequest = ns0.getBidLandscape_Dec().pyclass

getBidLandscapeResponse = ns0.getBidLandscapeResponse_Dec().pyclass
