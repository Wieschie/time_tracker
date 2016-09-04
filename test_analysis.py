import sys
from datetime import datetime
import pytz
from tzlocal import get_localzone
from datetime import datetime, timedelta

from logged_activity import Activity
import analysis


class TestParsing:
    local_tz = get_localzone()
    expected_list = [Activity(datetime(2016, 8, 24, 20, 4, 57, tzinfo=pytz.utc).astimezone(local_tz),
                              datetime(2016, 8, 24, 20, 29, 36, tzinfo=pytz.utc).astimezone(local_tz), 'p'),
                     Activity(datetime(2016, 8, 24, 20, 32, 19, tzinfo=pytz.utc).astimezone(local_tz),
                              datetime(2016, 8, 24, 21, 24, 39, tzinfo=pytz.utc).astimezone(local_tz), 'p'),
                     Activity(datetime(2016, 8, 25, 18, 33, 41, tzinfo=pytz.utc).astimezone(local_tz),
                              datetime(2016, 8, 25, 18, 45, 17, tzinfo=pytz.utc).astimezone(local_tz), 'g'),
                     Activity(datetime(2016, 8, 25, 18, 45, 17, tzinfo=pytz.utc).astimezone(local_tz),
                              datetime(2016, 8, 25, 18, 48, 53, tzinfo=pytz.utc).astimezone(local_tz), 'g')]

    def test_standard(self):
        f = open(sys.path[0] + "/tests/time_standard.log", 'r')
        assert analysis.parse_time_log(f) == self.expected_list

    def test_unfinished_activity(self):
        """ test the case where an activity is still ongoing """
        f = open("tests/time_unfinished.log", 'r')
        results_list = analysis.parse_time_log(f)
        for x in range(len(self.expected_list)):
            assert results_list[x] == self.expected_list[x]

        # the last event is ongoing so I can't test an exact end time
        expected_ongoing_dt_begin = datetime(2016, 8, 25, 18, 50, 53, tzinfo=pytz.utc).astimezone(self.local_tz)
        assert results_list[-1].dt_begin == expected_ongoing_dt_begin \
            and results_list[-1].activity_type == 'p' \
            and datetime.now().replace(tzinfo=self.local_tz) - results_list[-1].dt_end < timedelta(minutes=1)


class TestDaysTotaled:
    def test_get_days_totaled(self):
        assert 0


class TestPrintSummary:
    def test_print_day_summary(self):
        assert 0
