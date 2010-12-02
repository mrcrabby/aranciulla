################################################## 
# TrafficEstimatorService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from TrafficEstimatorService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class TrafficEstimatorServiceLocator:
    TrafficEstimatorInterface_address = "https://adwords.google.com:443/api/adwords/v13/TrafficEstimatorService"
    def getTrafficEstimatorInterfaceAddress(self):
        return TrafficEstimatorServiceLocator.TrafficEstimatorInterface_address
    def getTrafficEstimatorInterface(self, url=None, **kw):
        return TrafficEstimatorServiceSoapBindingSOAP(url or TrafficEstimatorServiceLocator.TrafficEstimatorInterface_address, **kw)

# Methods
class TrafficEstimatorServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: checkKeywordTraffic
    def checkKeywordTraffic(self, request):
        if isinstance(request, checkKeywordTrafficRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(checkKeywordTrafficResponse.typecode)
        return response

    # op: estimateAdGroupList
    def estimateAdGroupList(self, request):
        if isinstance(request, estimateAdGroupListRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(estimateAdGroupListResponse.typecode)
        return response

    # op: estimateCampaignList
    def estimateCampaignList(self, request):
        if isinstance(request, estimateCampaignListRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(estimateCampaignListResponse.typecode)
        return response

    # op: estimateKeywordList
    def estimateKeywordList(self, request):
        if isinstance(request, estimateKeywordListRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(estimateKeywordListResponse.typecode)
        return response

checkKeywordTrafficRequest = ns0.checkKeywordTraffic_Dec().pyclass

checkKeywordTrafficResponse = ns0.checkKeywordTrafficResponse_Dec().pyclass

estimateAdGroupListRequest = ns0.estimateAdGroupList_Dec().pyclass

estimateAdGroupListResponse = ns0.estimateAdGroupListResponse_Dec().pyclass

estimateCampaignListRequest = ns0.estimateCampaignList_Dec().pyclass

estimateCampaignListResponse = ns0.estimateCampaignListResponse_Dec().pyclass

estimateKeywordListRequest = ns0.estimateKeywordList_Dec().pyclass

estimateKeywordListResponse = ns0.estimateKeywordListResponse_Dec().pyclass
