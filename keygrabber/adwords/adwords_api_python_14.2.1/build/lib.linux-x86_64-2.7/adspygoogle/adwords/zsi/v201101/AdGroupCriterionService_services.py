################################################## 
# AdGroupCriterionService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from AdGroupCriterionService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class AdGroupCriterionServiceLocator:
    AdGroupCriterionServiceInterface_address = "https://adwords.google.com:443/api/adwords/cm/v201101/AdGroupCriterionService"
    def getAdGroupCriterionServiceInterfaceAddress(self):
        return AdGroupCriterionServiceLocator.AdGroupCriterionServiceInterface_address
    def getAdGroupCriterionServiceInterface(self, url=None, **kw):
        return AdGroupCriterionServiceSoapBindingSOAP(url or AdGroupCriterionServiceLocator.AdGroupCriterionServiceInterface_address, **kw)

# Methods
class AdGroupCriterionServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getAdGroupCriterion
    def getAdGroupCriterion(self, request):
        if isinstance(request, getAdGroupCriterionRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAdGroupCriterionResponse.typecode)
        return response

    # mutate: getAdGroupCriterion
    def mutateAdGroupCriterion(self, request):
        if isinstance(request, mutateAdGroupCriterionRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(mutateAdGroupCriterionResponse.typecode)
        return response

getAdGroupCriterionRequest = ns0.getAdGroupCriterion_Dec().pyclass

getAdGroupCriterionResponse = ns0.getAdGroupCriterionResponse_Dec().pyclass

mutateAdGroupCriterionRequest = ns0.mutateAdGroupCriterion_Dec().pyclass

mutateAdGroupCriterionResponse = ns0.mutateAdGroupCriterionResponse_Dec().pyclass
