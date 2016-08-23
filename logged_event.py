import datetime

class logged_event(object):
    
    def __init__(self, event_type, tag):
        self.time = datetime.datetime.now().isoformat()
        self.event_type = event_type
        self.tag = tag
        
