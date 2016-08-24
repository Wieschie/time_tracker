import httplib2
import os
import json
from collections import OrderedDict

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import consts

def upload(time, event_type):
    """ uploads a single event to google sheets

    """
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    
    ValueRange = {}
    ValueRange["range"]=consts.RANGE
    ValueRange["majorDimension"]="ROWS"
    ValueRange["values"]=[[time, event_type]]
    result = service.spreadsheets().values().append(
        spreadsheetId=consts.ID, range=consts.RANGE, valueInputOption='USER_ENTERED', body=ValueRange).execute()
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
    APPLICATION_NAME = consts.APP_NAME
    
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
    return credentials




