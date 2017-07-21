from datetime import datetime
from tzlocal import get_localzone
import pytz


class Event(object):
    
    def __init__(self, dt: datetime, activity_type: str):
        self.dt_begin = dt.replace(microsecond=0)
        self.tzinfo = get_localzone()
        self.activity_type = activity_type

    def __str__(self):
        return self.get_datetime_begin() + "," + str(self.get_offset()) + "," + self.activity_type

    # returns dt_begin as an iso formatted string.  Discard timezone info because all recorded times should
    # be in UTC
    def get_datetime_begin(self) -> str:
        return self.dt_begin.isoformat()[:-6]

    def get_localtime(self):
        return str(pytz.utc.localize(self.dt_begin).astimezone(self.tzinfo))

    def get_offset(self) -> float:
        return self.tzinfo.utcoffset(self.dt_begin).total_seconds()
