from argparse import Action
import sys
import pickle
from distutils.util import strtobool


class ActivityAction(Action):
    """ Custom argparse action that checks entered tag for typos by maintaining a persisted set of past entries """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(ActivityAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            accepted_activities = pickle.load(open(sys.path[0] + "/accepted_activities.p", 'rb'))
        except FileNotFoundError:
            accepted_activities = set()

        if values not in accepted_activities:
            if yesno("Activity not recognized. Add it?"):
                accepted_activities.add(values)
                pickle.dump(accepted_activities, open(sys.path[0] + "/accepted_activities.p", 'wb'))
            else:
                # quit if the user mistyped an activity tag
                exit()

        # save newly created datetime
        setattr(namespace, self.dest, values)


def yesno(question: str) -> bool:
    """ Simple yes/no prompt on screen """
    while 1:
        yn = input(question + " [y/N]")
        # treat No as the default
        if yn is '':
            return False
        try:
            return strtobool(yn)
        except ValueError:
            pass
