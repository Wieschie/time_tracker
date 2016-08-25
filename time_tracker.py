import argparse
from datetime import datetime

# Google Sheets API modules
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# project modules
from TimeAction import TimeAction
from logged_event import Event
from sheets_upload import upload


# takes an event and records it in a google sheet
def record_event_sheets(event: Event):
    upload(event)


def record_event_local(event: Event):
    f = open('time.log', 'a')
    f.write(str(event) + '\n')
    f.close()
    

if __name__ == '__main__':
    ### argument parsing
    parser = argparse.ArgumentParser(description='Track time spent on your computer.')
    # get activity type
    parser.add_argument('activity', default='g', nargs='?',
                        help='type of activity: gaming, tv, work, or finish (end tracking)', metavar='activity')
    # allow user to manually specify time
    parser.add_argument('-t', dest='time', required=False, action=TimeAction,
                        default=datetime.utcnow().replace(microsecond=0).isoformat(),
                        help="Manually specify a start time in 'HHMM' format")
    parser.add_argument('--test', dest='test', action='store_true', default=False,
                        help='"Dry run" that does not actually log an event.')
    flags = parser.parse_args()

    # create and record the event.
    e = Event(flags.activity, flags.time)
    print("Logging activity " + e.activity_type + " at " + e.datetime)
    if not flags.test:
        record_event_sheets(e)
        record_event_local(e)
