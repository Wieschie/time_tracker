from datetime import datetime, timedelta, date

from logged_event import Event


class Activity(Event):

    def __init__(self, dt_begin: datetime, dt_end: datetime, activity_type: str):
        super(Activity, self).__init__(dt_begin, activity_type)
        self.dt_end = dt_end

    def __str__(self):
        return super(Activity, self).__str__() + "," + self.dt_end

    def get_duration(self) -> timedelta:
        return self.dt_end - self.dt_begin

    def get_date(self) -> date:
        return self.dt_begin.date()
