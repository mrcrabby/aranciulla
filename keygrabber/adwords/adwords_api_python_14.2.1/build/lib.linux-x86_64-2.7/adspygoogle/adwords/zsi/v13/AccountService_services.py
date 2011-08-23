################################################## 
# AccountService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from AccountService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class AccountServiceLocator:
    AccountInterface_address = "https://adwords.google.com:443/api/adwords/v13/AccountService"
    def getAccountInterfaceAddress(self):
        return AccountServiceLocator.AccountInterface_address
    def getAccountInterface(self, url=None, **kw):
        return AccountServiceSoapBindingSOAP(url or AccountServiceLocator.AccountInterface_address, **kw)

# Methods
class AccountServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: getAccountInfo
    def getAccountInfo(self, request):
        if isinstance(request, getAccountInfoRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAccountInfoResponse.typecode)
        return response

    # op: getClientAccountInfos
    def getClientAccountInfos(self, request):
        if isinstance(request, getClientAccountInfosRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getClientAccountInfosResponse.typecode)
        return response

    # op: getClientAccounts
    def getClientAccounts(self, request):
        if isinstance(request, getClientAccountsRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getClientAccountsResponse.typecode)
        return response

    # op: getMccAlerts
    def getMccAlerts(self, request):
        if isinstance(request, getMccAlertsRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getMccAlertsResponse.typecode)
        return response

    # op: updateAccountInfo
    def updateAccountInfo(self, request):
        if isinstance(request, updateAccountInfoRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateAccountInfoResponse.typecode)
        return response

getAccountInfoRequest = ns0.getAccountInfo_Dec().pyclass

getAccountInfoResponse = ns0.getAccountInfoResponse_Dec().pyclass

getClientAccountInfosRequest = ns0.getClientAccountInfos_Dec().pyclass

getClientAccountInfosResponse = ns0.getClientAccountInfosResponse_Dec().pyclass

getClientAccountsRequest = ns0.getClientAccounts_Dec().pyclass

getClientAccountsResponse = ns0.getClientAccountsResponse_Dec().pyclass

getMccAlertsRequest = ns0.getMccAlerts_Dec().pyclass

getMccAlertsResponse = ns0.getMccAlertsResponse_Dec().pyclass

updateAccountInfoRequest = ns0.updateAccountInfo_Dec().pyclass

updateAccountInfoResponse = ns0.updateAccountInfoResponse_Dec().pyclass