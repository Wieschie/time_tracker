from collections import defaultdict
from datetime import timedelta

from sample.consts import DT_ZERO


class Day(object):
    """ custom data type that handles totalling a day's tracked time and printed formatting """
    def __init__(self, a=None, td=timedelta()):
        # can't use a mutable object as a default value.  default params are only evaluated when def is called,
        # and that happens precisely once, so it will return the exact same object each time.
        self.activities = defaultdict(lambda: timedelta()) if a is None else a
        self.total_td = td

    def add_activity(self, activity: str, time: timedelta):
        self.activities[activity] += time
        self.total_td += time

    def __str__(self):
        output = str()
        # print out activities in alphabetical order.  Just ensures they're in the same order each day.
        sorted_activities = sorted(self.activities)
        for a in sorted_activities:
            output += '\t{:8s} {:8s}'.format(str(a) + ": ", str((DT_ZERO + self.activities[a]).time())) + '\n'
        output += "\t" + '-' * 17 + '\n'
        output += "\ttotal:   " + str((self.total_td + DT_ZERO).time()) + '\n'
        return output

    # used in testing
    # TODO redefining __eq__ means hash needs to be redefined as well
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.activities == other.activities and self.total_td == other.total_td
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
