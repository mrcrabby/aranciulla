################################################## 
# CampaignTargetService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from CampaignTargetService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class CampaignTargetServiceLocator:
    CampaignTargetServiceInterface_address = "https://adwords.google.com:443/api/adwords/cm/v201101/CampaignTargetService"
    def getCampaignTargetServiceInterfaceAddress(self):
        return CampaignTargetServiceLocator.CampaignTargetServiceInterface_address
    def getCampaignTargetServiceInterface(self, url=None, **kw):
        return CampaignTargetServiceSoapBindingSOAP(url or CampaignTargetServiceLocator.CampaignTargetServiceInterface_address, **kw)

# Methods
class CampaignTargetServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getCampaignTarget
    def getCampaignTarget(self, request):
        if isinstance(request, getCampaignTargetRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getCampaignTargetResponse.typecode)
        return response

    # mutate: getCampaignTarget
    def mutateCampaignTarget(self, request):
        if isinstance(request, mutateCampaignTargetRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(mutateCampaignTargetResponse.typecode)
        return response

getCampaignTargetRequest = ns0.getCampaignTarget_Dec().pyclass

getCampaignTargetResponse = ns0.getCampaignTargetResponse_Dec().pyclass

mutateCampaignTargetRequest = ns0.mutateCampaignTarget_Dec().pyclass

mutateCampaignTargetResponse = ns0.mutateCampaignTargetResponse_Dec().pyclass
