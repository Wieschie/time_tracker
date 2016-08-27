from datetime import datetime


class Event(object):
    
    def __init__(self, dt: datetime, activity_type: str):
        self.dt_begin = dt
        self.activity_type = activity_type

    def __str__(self):
        return self.get_datetime_begin() + "," + self.activity_type

    # returns dt_begin as an iso formatted string.  Microseconds just aren't important to me.
    def get_datetime_begin(self) -> str:
        return self.dt_begin.replace(microsecond=0).isoformat()
