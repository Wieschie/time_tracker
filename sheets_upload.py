# from __future__ import print_function
import httplib2
import os
import json
from collections import OrderedDict 

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


def upload(time, event_type):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    # test sheet
    id = '1PDMqvbnSSwGrXdkeSqAVa9eMgJWZ2VwiulxnTSEZt9Y'
    r='Sheet1!A:B'

    ValueRange = {}
    ValueRange["range"]=r
    ValueRange["majorDimension"]="ROWS"
    ValueRange["values"]=[[time, event_type]]
    result = service.spreadsheets().values().append(
        spreadsheetId=id, range=r, valueInputOption='USER_ENTERED', body=ValueRange).execute()
    print(result)
    
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'python_time_tracker'
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-time_tracker.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials:
        raise Exception("Credentials have not been set up on this machine.")
    elif credentials.invalid:
        raise Exception("Credentials are invalid.")
#        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#        flow.user_agent = APPLICATION_NAME
#        if flags:
#            credentials = tools.run_flow(flow, store, flags)
#        else: # Needed only for compatibility with Python 2.6
#        credentials = tools.run(flow, store)
#        print('Storing credentials to ' + credential_path)
    return credentials




