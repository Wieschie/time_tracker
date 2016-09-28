from collections import defaultdict
from datetime import datetime

import pytz
from tzlocal import get_localzone
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sample.logged_activity import Activity
from sample.day_summary import Day



def parse_time_log(f) -> list:
    """
    :param f:  opened csv file handle of logged activities
    :return: list of Activity objects
    """

    # load time.log using list comprehension!
    # split incoming strings into tuple(datetime, activity_type).  datetime str is a fixed length -> just use indexes
    data = [(line.strip()[:19], line.strip()[20:]) for line in f]

    # until we hit an event tagged 'f', each time gap in events measures the duration of a certain activity
    # turn list of strings into list of Activity objects
    activities = []
    for i, event in enumerate(data):
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
    """
    :param activities: list of activities (like the one returned by parse_time_log)
    :return: dictionary in {datetime.date: Day} format
    """
    # group activities into days
    days = defaultdict(list)
    for a in activities:
        days[a.get_date()].append(a)
    # add all activities to respective Days
    days_totaled = defaultdict(lambda: Day())
    for day in days:
        days_totaled[day].set_date(day)
        for a in days[day]:
            days_totaled[day].add_activity(a.activity_type, a.get_duration())
    return days_totaled


def sort_days(days_totaled: defaultdict(lambda: Day), last_n_days: int) -> list:
    sorted_days_totaled = []
    # this results in a sorted list of datetimes.  Use this as a key to access days_totaled in sequential order.
    sorted_dates = sorted(days_totaled)
    for day in sorted_dates[-last_n_days:]:
        sorted_days_totaled.append(days_totaled[day])
    return sorted_days_totaled


def print_day_summary(sorted_days_totaled: list):
    """ print out a summary of activity totals per day """
    for day in sorted_days_totaled:
        print(day)


def graph_days(sorted_days_totaled: list):
    dates = [day.date for day in sorted_days_totaled]
    times = [day.total_td.total_seconds()/3600 for day in sorted_days_totaled]

    try:
        fig, ax = plt.subplots(1)
    except Exception as ex:
        print(ex)
        print("You may need to set a different backend in your matplotlibrc.  (try 'backend: agg')")
        exit()

    fig.autofmt_xdate()
    plt.title('Computer time')
    ax.bar(dates, times)
    plt.ylabel('Hours spent')
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.grid(b=True, which='major', axis='y', color='b', linestyle='-')
    plt.savefig('data/barchart.png', bbox_inches='tight')
