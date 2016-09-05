import pytz
from tzlocal import get_localzone
from datetime import datetime, timedelta, date

from logged_activity import Activity
import analysis

local_tz = get_localzone()
expected_activity_list = [Activity(datetime(2016, 8, 24, 20, 4, 57, tzinfo=pytz.utc).astimezone(local_tz),
                                   datetime(2016, 8, 24, 20, 29, 36, tzinfo=pytz.utc).astimezone(local_tz), 'p'),
                          Activity(datetime(2016, 8, 24, 20, 32, 19, tzinfo=pytz.utc).astimezone(local_tz),
                                   datetime(2016, 8, 24, 21, 24, 39, tzinfo=pytz.utc).astimezone(local_tz), 'p'),
                          Activity(datetime(2016, 8, 25, 18, 33, 41, tzinfo=pytz.utc).astimezone(local_tz),
                                   datetime(2016, 8, 25, 18, 45, 17, tzinfo=pytz.utc).astimezone(local_tz), 'g'),
                          Activity(datetime(2016, 8, 25, 18, 45, 17, tzinfo=pytz.utc).astimezone(local_tz),
                                   datetime(2016, 8, 25, 18, 48, 53, tzinfo=pytz.utc).astimezone(local_tz), 'g')]


class TestParsing:

    def test_standard(self):
        with open("tests/time_standard.log", 'r') as f:
            assert analysis.parse_time_log(f) == expected_activity_list

    def test_unfinished_activity(self):
        """ test the case where an activity is still ongoing """
        with open("tests/time_unfinished.log", 'r') as f:
            results_list = analysis.parse_time_log(f)

        for x in range(len(expected_activity_list)):
            assert results_list[x] == expected_activity_list[x]

        # the last event is ongoing so I can't test an exact end time
        expected_ongoing_dt_begin = datetime(2016, 8, 25, 18, 50, 53, tzinfo=pytz.utc).astimezone(local_tz)
        assert results_list[-1].dt_begin == expected_ongoing_dt_begin \
            and results_list[-1].activity_type == 'p' \
            and datetime.now().replace(tzinfo=local_tz) - results_list[-1].dt_end < timedelta(minutes=1)


class TestDaysTotaled:

    def test_get_days_totaled(self):
        expected_dates = [date(2016, 8, 24), date(2016, 8, 25)]
        expected_activity_types = ['p', 'g']
        expected_td = [timedelta(hours=1, minutes=16, seconds=59), timedelta(minutes=15, seconds=12)]

        results = analysis.get_days_totaled(expected_activity_list)
        assert set(results.keys()) == set(expected_dates)

        for ed, ea, et in zip(expected_dates, expected_activity_types, expected_td):
            assert list(results[ed].activities)[0] == ea
            assert results[ed].activities[ea] == et
            assert results[ed].total_td == et


class TestPrintSummary:
    def test_print_day_summary(self):
        assert 0
