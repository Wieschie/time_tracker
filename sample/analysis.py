from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches

from sample.logged_activity import Activity
from sample.day_summary import Day


def parse_time_log(f) -> list:
    """
    :param f:  opened csv file handle of logged activities
    :return: list of Activity objects
    """

    # load time.log using list comprehension!
    # [datetime, timezone name, activity name]
    data = [line.split(',') for line in f]

    # until we hit an event tagged 'f', each time gap in events measures the duration of a certain activity
    # turn list of strings into list of Activity objects
    activities = []
    for i, event in enumerate(data):
        # events tagged 'f' are just the user logging off.  Do not treat as the start of a new activity
        if event[2] is not 'f':
            fmt = "%Y-%m-%dT%H:%M:%S"
            dt_begin = datetime.strptime(event[0], fmt)
            if i != len(data) - 1:
                dt_end = datetime.strptime(data[i+1][0], fmt)
            # the last event isn't marked as 'f', so it's ongoing.  We can total the time up until now.
            else:
                dt_end = datetime.utcnow().replace(microsecond=0)
            activity_type = event[2]
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


def draw_daymap(activity_list: list):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis([275, 300, 0, 60*24])
    plt.ylabel('Time of day')

    # TODO handle activities spanning across days
    for a in activity_list:
        t = a.dt_end.time()
        rt = t.hour * 60 + t.minute
        d = round(a.get_duration().total_seconds()/60)

        # date handling is way off but as a prototype it gets the point across
        ax.add_patch(patches.Rectangle((31*a.get_date().month + a.get_date().day, rt), 0.75, d))

    plt.savefig('data/heatmap.png', bbox_inches='tight')
