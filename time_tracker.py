import argparse
from datetime import datetime

from TimeAction import TimeAction
import logged_event
from sheets_upload import upload


from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


# takes an event and records it in a google sheet
def record_event_sheets(event):
    upload(event)


def record_event_local(event):
    f = open('time.log', 'a')
    f.write(event + '\n')
    f.close()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Track time spent on your computer.')

    # get activity type
    parser.add_argument('activity', default='g', nargs='?',
                        help='type of activity: gaming, tv, work, or finish (end tracking)', metavar='activity')

    # allow user to manually specify time
    parser.add_argument('-t', dest='time', required=False, action=TimeAction,
                        default=datetime.utcnow().replace(microsecond=0).isoformat(),
                        help="Manually specify a start time in 'HHMM' format")

    parser.add_argument('--test', dest='test', action='store_true', default=False)

    flags = parser.parse_args()
    
    e = logged_event.Event(flags.activity, flags.time)

    print(e)
    if not flags.test:
        record_event_sheets(e)
        record_event_local(str(e))
