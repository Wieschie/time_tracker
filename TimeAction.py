# Custom argparse action that validates a user-entered time and converts to a datetime object with the current date.

from argparse import Action
from datetime import datetime

class TimeAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(TimeAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            d = datetime.strptime(values, "%H%M")
        except ValueError:
            print("Invalid time entered.")
            exit()

        # Only accepts HHMM from user, so add current date to event
        n = datetime.now()
        d = d.replace(year=n.year, month=n.month, day=n.day)

        # save newly created datetime
        setattr(namespace, self.dest, str(d))
