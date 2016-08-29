from collections import defaultdict
from datetime import datetime, timedelta

import pytz
from tzlocal import get_localzone

from logged_activity import Activity


def parse_time_log() -> list:
    """ Parses the local time.log file and returns a list of Activity objects (one per line) """
    f = open("time.log", 'r')
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


def get_days_totaled(activities: list) -> defaultdict(lambda: defaultdict(lambda: timedelta())):
    """ Sums all instances of each activity in a day and returns as a {day: {activity_type: duration}} defaultdict """
    # group activities into days
    days = defaultdict(list)
    for a in activities:
        days[a.get_date()].append(a)

    # combine multiple occurrences of an activity within each day to get a total time per activity per day
    # lambda is required because defaultdict needs a callable.
    # dictionary elements look like {day(str): {activity_type(str): duration(timedelta}}
    days_totaled = defaultdict(lambda: defaultdict(lambda: timedelta()))
    for day in days:
        for a in days[day]:
            # TODO use activity addition here? might work without changes to Activity
            # https://docs.python.org/3/reference/datamodel.html#object.__iadd__
            days_totaled[day][a.activity_type] += a.get_duration()
    return days_totaled


def print_day_summary(activities: list):
    days_totaled = get_days_totaled(activities)
    # print out a summary of activity totals per day
    for day in days_totaled:
        print(day.isoformat() + ":")

        for activity in days_totaled[day]:
            # days_totaled[day][activity] is length of a given activity in seconds.
            # Using timedelta to convert to HH:MM:SS
            print('\t' + '{:8s} {:8s}'.format(str(activity) + ": ",
                                              str((datetime(1970, 1, 1) + days_totaled[day][activity]).time())))


if __name__ == '__main__':
    activity_list = parse_time_log()
    print_day_summary(activity_list)
