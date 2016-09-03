import argparse
from collections import defaultdict
from datetime import datetime

import pytz
from tzlocal import get_localzone

from logged_activity import Activity
from day_summary import Day


def parse_time_log(f) -> list:
    """ Parses the local time.log file and returns a list of Activity objects (one per line) """
    # load time.log using list comprehension!
    # split incoming strings into tuple(datetime, activity_type).  datetime str is a fixed length -> just use indexes
    data = [(line.strip()[:19], line.strip()[20:]) for line in f]
    f.close()

    # until we hit an event tagged 'f', each time gap in events measures the duration of a certain activity
    # turn list of strings into list of Activity objects
    activities = []
    for i, event in enumerate(data):
        # don't treat the last event in the log as the start of an activity.
        # events tagged 'f' are just the user logging off.  Do not treat as the start of a new activity
        if event[1] is not 'f':
            # TODO all datetimes are stored in UTC. store tzinfo?
            # Convert to local timezone.  credit to:
            # http://stackoverflow.com/a/18569497/1706825
            # http://stackoverflow.com/a/4530166/1706825
            local_tz = get_localzone()
            fmt = "%Y-%m-%dT%H:%M:%S"
            dt_begin = datetime.strptime(event[0], fmt).replace(tzinfo=pytz.utc).astimezone(local_tz)
            if i != len(data) - 1:
                dt_end = datetime.strptime(data[i+1][0], fmt).replace(tzinfo=pytz.utc).astimezone(local_tz)
            # the last event isn't marked as 'f', so it's ongoing.  We can total the time up until now.
            else:
                dt_end = datetime.now().replace(microsecond=0, tzinfo=local_tz)
            activity_type = event[1]
            activities.append(Activity(dt_begin, dt_end, activity_type))
    return activities


def get_days_totaled(activities: list) -> defaultdict(lambda: Day):
    """ Sums all instances of each activity in a day and returns as a {day: {activity_type: duration}} """
    # group activities into days
    days = defaultdict(list)
    for a in activities:
        days[a.get_date()].append(a)
    # combine multiple occurrences of an activity within each day to get a total time per activity per day
    # TODO want to use OrderedDict for the outer container as dates are already in order.  But it doesn't support
    # nesting.  Extend it myself?
    # lambda is required because defaultdict needs a callable.
    # dictionary elements look like {day(str): {activity_type(str): duration(timedelta}}
    days_totaled = defaultdict(lambda: Day())
    for day in days:
        for a in days[day]:
            days_totaled[day].add_activity(a.activity_type, a.get_duration())
    return days_totaled


def print_day_summary(activities: list, last_n_days=None):
    """ print out a summary of activity totals per day """
    if type(last_n_days) is int:
        last_n_days *= -1
    days_totaled = get_days_totaled(activities)
    # this results in a sorted list of datetimes.  Use this as a key to access days_totaled in sequential order.
    sorted_days = sorted(days_totaled)
    for day in sorted_days[last_n_days:]:
        print(day.strftime("%a %b %d") + ":")
        print(days_totaled[day])


if __name__ == '__main__':
    # TODO parse some args
    parser = argparse.ArgumentParser(description='Analyze time.log.')
    parser.add_argument('-n', dest='last_n_days', help="Display a summary of the last n days.", type=int, default=None)
    flags = parser.parse_args()
    log = open("time.log", 'r')
    activity_list = parse_time_log(log)
    print_day_summary(activity_list, flags.last_n_days)
