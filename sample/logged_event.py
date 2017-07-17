from datetime import datetime
from tzlocal import get_localzone
import pytz


class Event(object):
    
    def __init__(self, dt: datetime, activity_type: str):
        self.dt_begin = pytz.utc.localize(dt.replace(microsecond=0))
        self.tzinfo = get_localzone()
        self.activity_type = activity_type

    def __str__(self):
        return self.get_datetime_begin() + "," + str(self.tzinfo) + "," + self.activity_type

    # returns dt_begin as an iso formatted string.  Microseconds just aren't important to me.
    def get_datetime_begin(self) -> str:
        return self.dt_begin.isoformat()

    def get_localtime(self):
        return str(self.dt_begin.astimezone(self.tzinfo))
