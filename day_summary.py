from collections import defaultdict
from datetime import datetime, timedelta

from consts import DT_ZERO


class Day(object):
    """ custom data type to store information on a day in the life of the user """
    def __init__(self):
        self.activities = defaultdict(lambda: timedelta())
        self.total_td = DT_ZERO

    def add_activity(self, activity: str, time: timedelta):
        self.activities[activity] = time
        self.total_td += time

    def __str__(self):
        output = str()
        for a in self.activities:
            output += ('\t{:8s} {:8s}'.format(str(a) + ": ", str((DT_ZERO + self.activities[a]).time())))
        output += ("\n\t" + '-' * 17)
        output += "\n\ttotal:   " + str(self.total_td.time()) + '\n'
        return output
