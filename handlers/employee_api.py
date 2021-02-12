import requests
import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import urllib3
from datetime import datetime

EMPLOYEE_API = 'https://api.fmgl.com.au/employee/'
TOKEN_URL='https://login.microsoftonline.com/143a7396-a856-47d7-8e31-62990b5bacd0/oauth2/v2.0/token'
CLIENT_ID = '9fe04cd6-4363-445d-b1f6-064ce28ae649'
SECRET = 'OuN0TqY0M8Y~xr6B.xC-5k0w~yPcGB9IEe'
SCOPE = ['api://eff7d01f-be35-4e84-ab45-d317d291af4f/.default']


# this uses the SucessFactors API 
class EmployeeAPI(object):


    def __init__(self, SAPId):
        self._SAPId=SAPId 
    
    def getHttpsEndpoint(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        https=urllib3.PoolManager(cert_reqs='CERT_NONE')
        return https

    def getAccessToken(self):
        # Fetch Access Token from Azure
        client = BackendApplicationClient(client_id=CLIENT_ID)
        oauth = OAuth2Session(client=client)
        tokens = oauth.fetch_token(token_url=TOKEN_URL, client_secret=SECRET, scope=SCOPE)

        access_token = tokens['access_token']
        return access_token

    def getPersonDetails(self,https,api_headers,personId):
        restUrl='{}{}'.format(EMPLOYEE_API,personId)
        r=https.request('GET',restUrl,headers =api_headers )
        response= r.data.decode('utf-8')
        return json.loads(response)

    def getBoth(self,access_token,employeeId):

        api_headers = {
            'Authorization': 'Bearer ' + access_token
        }

        https=self.getHttpsEndpoint()

        # get Employee record
        employee = self.getPersonDetails(https,api_headers,employeeId)

        # get supervisor record
        supervisorId =employee['job']['managerId']
        supervisor = self.getPersonDetails(https,api_headers,supervisorId)

        return {
            'employee': employee,
            'supervisor': supervisor
        }

    def getEmployeeAndSupervisor(self):                
             
        access_token=self.getAccessToken()
        print(access_token)

        # Fetch employee details
        persons=self.getBoth(access_token,self._SAPId)
        return persons
        