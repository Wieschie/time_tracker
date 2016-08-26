from datetime import datetime, timedelta
from logged_activity import Activity


# start working with local file only
def parse_activities():
    # TODO implement some sort of log rotation and caching each time analysis is run
    # load time.log using list comprehension!
    f = open("time.log", 'r')
    # split incoming strings into tuple(datetime, activity_type).  datetime str is a fixed length -> just use indexes
    data = [(line.strip()[:19], line.strip()[21:]) for line in f]
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

    print("Activity type, duration (MM:SS):")
    for a in activities:
        print(a.activity_type + ", %d:%d" % divmod(a.get_duration().total_seconds(), 60))


# TODO fill stub
def last_event():
    return

if __name__ == '__main__':
    parse_activities()
