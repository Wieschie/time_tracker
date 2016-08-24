import datetime


class Event(object):
    
    def __init__(self, atype, dt=datetime.datetime.utcnow().isoformat()):
        self.datetime = dt
        self.activity_type = atype

    def __str__(self):
        return self.datetime + ", " + self.activity_type
