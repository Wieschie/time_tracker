import argparse
import logged_event
from sheets_upload import upload

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# takes an event and records it in a google sheet
def record_event_sheets(e):
    print(e.__dict__)
    upload(e.time, e.event_type)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Track time spent on your computer.')

    # get activity type
    parser.add_argument('activity', choices=['g', 't', 'w', 'f'], default='g', help='type of activity: gaming, tv, work, or finish (end tracking)', metavar='activity')
    
    # assume a task is starting if no flag provided
    # parser.add_argument('-f', dest='finish', default=False, action='store_true', help='finish a task')
    
    flags = parser.parse_args()
    
    e = logged_event.event(flags.activity)

    record_event_sheets(e)
    

