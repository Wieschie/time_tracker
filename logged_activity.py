from logged_event import Event
from datetime import datetime


class Activity(Event):

    def __init__(self, dt: datetime, atype: str, duration: time):
        super(Activity, self).__init__(dt, atype)
        self.duration = duration

    def __str__(self):
        return super(Activity, self).__str__() + ", " + self.duration
