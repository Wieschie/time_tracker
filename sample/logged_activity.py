from datetime import datetime, timedelta, date
import pytz

from sample.logged_event import Event


class Activity(Event):

    def __init__(self, dt_begin: datetime, dt_end: datetime, activity_type: str):
        super(Activity, self).__init__(dt_begin, activity_type)
        self.dt_end = pytz.utc.localize(dt_end)

    def __str__(self):
        return self.get_datetime_begin() + "," + self.get_datetime_end() + "," + self.activity_type

    # adding two activities just checks to make sure the tag is the same and then returns total duration
    # TODO make this useful or delete it
    def __add__(self, other) -> timedelta:
        if isinstance(other, Activity):
            if self.activity_type != other.activity_type:
                raise UserWarning("Activity types do not match.  Are you sure you want to add them?")
            return self.get_duration() + other.get_duration()
        if isinstance(other, timedelta):
            return self.get_duration() + other
        else:
            return NotImplemented

    # used in testing
    # TODO redefining __eq__ means hash needs to be redefined as well
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.dt_begin == other.dt_begin \
                   and self.dt_end == other.dt_end \
                   and self.activity_type == other.activity_type
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    # returns dt_begin as an iso formatted string.  Microseconds just aren't important to me.
    def get_datetime_end(self) -> str:
        return self.dt_end.replace(microsecond=0).isoformat()

    def get_duration(self) -> timedelta:
        return self.dt_end - self.dt_begin

    def get_date(self) -> date:
        return self.dt_begin.date()
