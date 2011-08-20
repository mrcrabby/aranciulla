################################################## 
# DataService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from DataService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class DataServiceLocator:
    DataServiceInterface_address = "https://adwords.google.com:443/api/adwords/cm/v201101/DataService"
    def getDataServiceInterfaceAddress(self):
        return DataServiceLocator.DataServiceInterface_address
    def getDataServiceInterface(self, url=None, **kw):
        return DataServiceSoapBindingSOAP(url or DataServiceLocator.DataServiceInterface_address, **kw)

# Methods
class DataServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getDataAdGroupBidLandscape
    def getAdGroupBidLandscape(self, request):
        if isinstance(request, getAdGroupBidLandscapeRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAdGroupBidLandscapeResponse.typecode)
        return response

    # get: getDataCriterionBidLandscape
    def getCriterionBidLandscape(self, request):
        if isinstance(request, getCriterionBidLandscapeRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getCriterionBidLandscapeResponse.typecode)
        return response

getAdGroupBidLandscapeRequest = ns0.getAdGroupBidLandscape_Dec().pyclass

getAdGroupBidLandscapeResponse = ns0.getAdGroupBidLandscapeResponse_Dec().pyclass

getCriterionBidLandscapeRequest = ns0.getCriterionBidLandscape_Dec().pyclass

getCriterionBidLandscapeResponse = ns0.getCriterionBidLandscapeResponse_Dec().pyclass
