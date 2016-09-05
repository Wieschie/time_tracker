import argparse
from sample.analysis import parse_time_log, print_day_summary

if __name__ == '__main__':
    # TODO parse some args
    parser = argparse.ArgumentParser(description='Analyze time.log.')
    parser.add_argument('-n', dest='last_n_days', help="Display a summary of the last n days.", type=int, default=None)
    parser.add_argument('-f', dest='filename', help="Specify a log file to analyze.", type=str, default="sample/time.log")
    flags = parser.parse_args()
    with open(flags.filename, 'r') as log:
        activity_list = parse_time_log(log)
    print_day_summary(activity_list, flags.last_n_days)
