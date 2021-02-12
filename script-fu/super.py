# - pip3 install oauthlib
# - pip3 install requests_oauthlib
import json
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import urllib3
from datetime import datetime

EMPLOYEE_API = 'https://api.fmgl.com.au/employee/'
TOKEN_URL='https://login.microsoftonline.com/143a7396-a856-47d7-8e31-62990b5bacd0/oauth2/v2.0/token'
CLIENT_ID = '9fe04cd6-4363-445d-b1f6-064ce28ae649'
SECRET = 'OuN0TqY0M8Y~xr6B.xC-5k0w~yPcGB9IEe'
SCOPE = ['api://eff7d01f-be35-4e84-ab45-d317d291af4f/.default']

def getHttpsEndpoint():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    https=urllib3.PoolManager(cert_reqs='CERT_NONE')
    return https

def getAccessToken():
    # Fetch Access Token from Azure
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    tokens = oauth.fetch_token(token_url=TOKEN_URL, client_secret=SECRET, scope=SCOPE)

    access_token = tokens['access_token']
    return access_token

def getPersonDetails( https,api_headers,personId):
    restUrl='{}{}'.format(EMPLOYEE_API,personId)
    r=https.request('GET',restUrl,headers =api_headers )
    response= r.data.decode('utf-8')
    return json.loads(response)


def getBothPersons(access_token,employeeId):

    api_headers = {
        'Authorization': 'Bearer ' + access_token
    }

    https=getHttpsEndpoint()

    # get Employee record
    employee = getPersonDetails(https,api_headers,employeeId)

    # get supervisor record
    supervisorId =employee['job']['managerId']
    supervisor = getPersonDetails(https,api_headers,supervisorId)

    return {
        'employee': employee,
        'supervisor': supervisor
    }

def main():

    employeeId='589232'
    access_token=getAccessToken()

    # Fetch employee details

    persons=getBothPersons(access_token,employeeId)
    print(json.dumps(persons,indent=4))


if __name__ == "__main__":
    main()