import httplib2
import os

from apiclient import discovery
import oauth2client

from sample import consts
from sample.logged_event import Event


def upload(event: Event) -> object:
    # uploads a single event to google sheets

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                     'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discovery_url)
    # build the request body
    value_range = {
        "range": consts.RANGE,
        "majorDimension": "ROWS",
        "values": [[event.get_datetime_begin(), event.tzinfo(), event.activity_type]]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=consts.ID, range=consts.RANGE, valueInputOption='USER_ENTERED', body=value_range).execute()

    # TODO - figure out failure response from API and handle it
    # sample result: {'spreadsheetId': 'id', 'tableRange': 'experimental!A1:B57', 'updates': {'spreadsheetId': 'id',
    # 'updatedRange': 'experimental!A58:B58', 'updatedRows': 1, 'updatedCells': 2, 'updatedColumns': 2}}
    print(str(result['updates']['updatedRows']) + " row(s) updated in Google Sheets.")


def get_credentials():
    """ Taken from Google's quick start script

    Gets valid user credentials from storage.

    CURRENTLY DOES NOT WORK:
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

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
