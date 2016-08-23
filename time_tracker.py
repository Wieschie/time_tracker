import argparse
import logged_event

parser = argparse.ArgumentParser(description='Track time spent on your computer.')

# assume a task is starting if no flag provided
parser.add_argument('-f', dest='finish', default=False, help='finish a task')

# get activity type
parser.add_argument('activity', choices=['g', 't', 'w'], default='g', nargs=1, help='type of activity', metavar='activity')

flags = parser.parse_args()

print(flags)



