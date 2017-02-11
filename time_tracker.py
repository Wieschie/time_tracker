import argparse
import sys
from datetime import datetime
import os
import time
import sqlite3

from sample.TimeAction import TimeAction
from sample.ActivityAction import ActivityAction
from sample.logged_event import Event
from sample.sheets_upload import upload


def record_event_sheets(event: Event):
    """ appends the event to a google sheet """
    upload(event)


def record_event_local(event: Event):
    """ writes event in plaintext to a local logfile """
    # sys.path[0] is the directory of this script.  http://stackoverflow.com/a/5475224/1706825
    f = open(sys.path[0] + '/data/time.log', 'a')
    f.write('\n' + str(event))
    f.close()


def record_event_sqlite(event: Event):
    """ records event in a local sqlite db """
    conn = sqlite3.connect(sys.path[0] + '/data/time.db')
    c = conn.cursor()

    # check if events table exists and create one if needed
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    if c.fetchone() is None:
        init_sqlite_db(conn)


def init_sqlite_db(conn: sqlite3.Connection):
    """ creates a table with the desired schema for storing events """
    conn.execute("(CREATE TABLE events (timestamp text, activity_type text, tz text)")
    conn.commit()


def remind(mins: int):
    """ Rings terminal bell and prints reminder message """
    time.sleep(mins)
    print('\a\nYour time is up!  \nYou will still need to log the end of your activity.')
    time.sleep(1)
    print('\a', end='')
    exit()

if __name__ == '__main__':
    # ---- argument parsing -----
    parser = argparse.ArgumentParser(description='Track time spent on your computer.')
    # get activity type: string entered directly after command
    parser.add_argument('activity', nargs='?', help='type of activity', action=ActivityAction)
    # allow user to manually specify time
    parser.add_argument('-t', dest='time', required=False, action=TimeAction, default=datetime.utcnow(),
                        help="Manually specify a start time in 'HHMM' format")
    parser.add_argument('--test', dest='test', action='store_true', default=False,
                        help='"Dry run" that does not actually log an event.')
    parser.add_argument('-r', dest='remind_time', type=int, default=0,
                        help='Remind you in n minutes that your time is up.')
    flags = parser.parse_args()

    # create and record the event.
    e = Event(flags.time, flags.activity)
    print("Logging activity: '" + e.activity_type + "' at " + e.get_datetime_begin() + "UTC")
    if not flags.test:
        record_event_sheets(e)
        record_event_local(e)

    # if a reminder is set, fork and run that reminder in the background
    if flags.remind_time:
        child_pid = os.fork()
        if child_pid:
            print("You will be reminded in {} minutes!".format(flags.remind_time))
        else:
            remind(flags.remind_time)

