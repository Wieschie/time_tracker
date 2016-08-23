import argparse
import logged_event

parser = argparse.ArgumentParser(description='Track time spent on your computer.')

# get activity type
parser.add_argument('activity', choices=['g', 't', 'w'], default='g', help='type of activity', metavar='activity')

# assume a task is starting if no flag provided
parser.add_argument('-f', dest='finish', default=False, action='store_true', help='finish a task')

flags = parser.parse_args()

print(flags)



