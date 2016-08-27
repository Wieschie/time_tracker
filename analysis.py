from datetime import datetime, timedelta
from collections import defaultdict, Counter

from logged_activity import Activity


# start working with local file only
def parse_activities():
    # TODO implement some sort of log rotation and caching each time analysis is run
    # load time.log using list comprehension!
    f = open("time.log", 'r')
    # split incoming strings into tuple(datetime, activity_type).  datetime str is a fixed length -> just use indexes
    data = [(line.strip()[:19], line.strip()[20:]) for line in f]
    f.close()

    # until we hit an event tagged 'f', each time gap in events measures the duration of a certain activity
    # turn list of strings into list of Activity objects
    activities = []
    for i, event in enumerate(data):
        # don't treat the last event in the log as the start of an activity.
        # events tagged 'f' are just the user logging off.  Do not treat as the start of a new activity
        if i != len(data) - 1 and event[1] is not 'f':
            dt_begin = datetime.strptime(event[0], "%Y-%m-%dT%H:%M:%S")
            dt_end = datetime.strptime(data[i+1][0], "%Y-%m-%dT%H:%M:%S")
            activity_type = event[1]
            activities.append(Activity(dt_begin, dt_end, activity_type))

    # group activities into days
    days = defaultdict(list)
    for a in activities:
    	# TODO convert back to local timezone here?  should I be storing timezone data as well?
	days[a.get_date()].append(a)

    # combine multiple occurrences of an activity within each day to get a total time per activity per day
    days_totaled = defaultdict(lambda: Counter())
    for day in days:
        for a in days[day]:
            # TODO use activity addition here? might work without changes to Activity
            # https://docs.python.org/3/reference/datamodel.html#object.__iadd__
            days_totaled[day][a.activity_type] += a.get_duration().total_seconds()

    # print out a summary of activity totals per day
    for day in days_totaled:
        print(day.isoformat() + ":")
        for activity in days_totaled[day]:
            # days_totaled[day][activity] is length of a given activity in seconds.
            # Using timedelta to convert to HH:MM:SS
            print('\t' + '{:8s} {:8s}'.format(str(activity) + ": ",
                  str((datetime(1970, 1, 1) + timedelta(seconds=days_totaled[day][activity])).time())))


# TODO fill stub
def last_event():
    return

if __name__ == '__main__':
    parse_activities()
