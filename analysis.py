from datetime import datetime, date, time


# start working with local file only
f = open("time.log", "r")

# read the logfile line by line!
# @TODO implement some sort of log rotation and caching each time analysis is run

# session is used to track activity switching during the same usage session
session = []
for line in f:
    dt = datetime.strptime(line, "%Y-%m-%dT%H:%M:%S")
