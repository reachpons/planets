# Mock attempt at returning an OAuth2 (Authorization Code flow) bearer token
__author__ = 'Patrick Glynn'

import requests, json
import subprocess
import sys

authorize_url = "https://login.microsoftonline.com/143a7396-a856-47d7-8e31-62990b5bacd0/oauth2/v2.0/authorize"
token_url = "https://login.microsoftonline.com/143a7396-a856-47d7-8e31-62990b5bacd0/oauth2/v2.0/token"

# Callback url specified when the application was defined
callback_uri = "http://localhost"

test_api_url = "https://api.fmgl.com.au/employee/589232"

# Client (application) credentials - from Azure App Registration
client_id = 'eff7d01f-be35-4e84-ab45-d317d291af4f'
client_secret = 'Zz60bFtkungUnDx~hdLi89~L-_7OJru6ug'

scope='openid profile email offline_access api://eff7d01f-be35-4e84-ab45-d317d291af4f/Employee.API.Get'

# Simulate a request from a browser to the authorize_url - will return an authorization code after the user is prompted for credentials
authorization_redirect_url = authorize_url + '?response_type=code&client_id=' + client_id + '&redirect_uri=' + callback_uri + '&scope=' + scope

# This part is still a question mark, how do we pass an authenticated session instead of manual intervention?
print("Copy the following url into a browser session and enter the code from the returned url: ")
print("---  " + authorization_redirect_url + "  ---")
authorization_code = input('code: ')

# Turn the authorization code into a access token, etc
data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
print("requesting access token")
access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

print("response")
print(access_token_response.headers)
print('body: ' + access_token_response.text)

# We can now use the access_token as much as we want to access protected resources.
tokens = json.loads(access_token_response.text)
access_token = tokens['access_token']
print("access token: " + access_token)

api_call_headers = {'Authorization': 'Bearer ' + access_token}
api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)

print(api_call_response.text)