from collections import defaultdict
from datetime import timedelta

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
        # print out activities in alphabetical order.  Just ensures they're in the same order each day.
        sorted_activities = sorted(self.activities)
        for a in sorted_activities:
            output += '\t{:8s} {:8s}'.format(str(a) + ": ", str((DT_ZERO + self.activities[a]).time())) + '\n'
        output += "\t" + '-' * 17 + '\n'
        output += "\ttotal:   " + str(self.total_td.time()) + '\n'
        return output
