from datetime import datetime


class Event(object):
    
    def __init__(self, dt: datetime, atype: str):
        self.dt_begin = dt
        self.activity_type = atype

    def __str__(self):
        return self.get_datetime() + ", " + self.activity_type

    # returns datetime as an iso formatted string
    def get_datetime(self) -> str:
        return self.dt_begin.replace(microsecond=0).isoformat()
