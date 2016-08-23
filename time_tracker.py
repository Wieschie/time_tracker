import argparse
import logged_event

# takes an event and records it
def record_event(e):
    print(e.__dict__)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Track time spent on your computer.')

    # get activity type
    parser.add_argument('activity', choices=['g', 't', 'w', 'f'], default='g',
                        help='type of activity: gaming, tv, work, or finish (end tracking)', metavar='activity')
    
    # assume a task is starting if no flag provided
    # parser.add_argument('-f', dest='finish', default=False, action='store_true', help='finish a task')
    
    flags = parser.parse_args()
    
    e = logged_event.event(flags.activity)

    record_event(e)
    

