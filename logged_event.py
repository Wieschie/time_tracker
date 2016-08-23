import datetime

class event(object):
    
    def __init__(self, event_type):
        self.time = datetime.datetime.now().isoformat()
        self.event_type = event_type
        # no tags for now
        #self.tag = tag
    
