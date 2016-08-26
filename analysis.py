from datetime import datetime, date, time, timedelta


# start working with local file only
def parse_activities():
    # @TODO implement some sort of log rotation and caching each time analysis is run
    # load time log using list comprehension!
    f = open("time.log", 'r')
    data = [line.strip() for line in f]
    f.close()

    # until we hit an event tagged 'f', each time gap in events measures the duration of a certain activity
    # turn list of strings into list of Activity objects
    activities = []
    for i, event in enumerate(data):
    # don't treat the last event in the log as the start of an activity.
        if i != len(event) - 1:
            dt = datetime.strptime(event, "%Y-%m-%dT%H:%M:%S")


# TODO fill stub
def last_event():
    return
