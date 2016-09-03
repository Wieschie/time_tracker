import pytest
import analysis
from datetime import datetime
import pytz

from logged_activity import Activity


class TestParsing:
    def test_standard(self):
        f = open("test/time_standard.log", 'r')
        # set up expected return values
        cst = pytz.timezone("America/Chicago")
        expected_list = [Activity(datetime(2016, 8, 24, 15, 4, 57, cst), datetime(2016, 8, 24, 15, 29, 36, cst), 'p'),
                         Activity(datetime(2016, 8, 24, 15, 32, 19, cst), datetime(2016, 8, 24, 16, 24, 39, cst), 'p'),
                         Activity(datetime(2016, 8, 25, 13, 33, 41, cst), datetime(2016, 8, 25, 13, 45, 17, cst), 'g'),
                         Activity(datetime(2016, 8, 25, 13, 45, 17, cst), datetime(2016, 8, 25, 13, 48, 53, cst), 'g')]

        assert analysis.parse_time_log(f) == expected_list

    def test_unfinished_activity(self):
        """ test the case where an activity is still ongoing """
        f = open("test/time_unfinished.log", 'r')
        expected_list = []
        assert analysis.parse_time_log(f) == expected_list


class TestDaysTotaled:
    def test_get_days_totaled(self):
        assert 0


class TestPrintSummary:
    def test_print_day_summary(self):
        assert 0
