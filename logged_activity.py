from datetime import datetime, timedelta, date

from logged_event import Event


class Activity(Event):

    def __init__(self, dt_begin: datetime, dt_end: datetime, activity_type: str):
        super(Activity, self).__init__(dt_begin, activity_type)
        self.dt_end = dt_end

    def __str__(self):
        return super(Activity, self).__str__() + "," + self.dt_end

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

    def get_duration(self) -> timedelta:
        return self.dt_end - self.dt_begin

    def get_date(self) -> date:
        return self.dt_begin.date()
