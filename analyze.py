#!/usr/bin/python3

import argparse
import sample.analysis as analysis

if __name__ == '__main__':
    # TODO parse some args
    parser = argparse.ArgumentParser(description='Analyze time.log.')
    parser.add_argument('-n', dest='last_n_days', help="Analyze the last n days only.", type=int, default=0)
    parser.add_argument('-f', dest='filename', help="Specify a log file to analyze.", type=str, default="data/time.log")
    flags = parser.parse_args()
    with open(flags.filename, 'r') as log:
        activity_list = analysis.parse_time_log(log)

    # datetime: Day dictionary
    days_totaled = analysis.get_days_totaled(activity_list)
    # sorted list of Days
    sorted_days_totaled = analysis.sort_days(days_totaled, flags.last_n_days)

    analysis.print_day_summary(sorted_days_totaled)
    analysis.graph_days(sorted_days_totaled)
