from datetime import datetime


class Event(object):
    
    def __init__(self, dt: datetime, atype: str):
        self.dt = dt
        self.activity_type = atype

    def __str__(self):
        return self.get_datetime() + ", " + self.activity_type

    # returns datetime as an iso formatted string
    def get_datetime(self) -> str:
        return self.dt.replace(microsecond=0).isoformat()
