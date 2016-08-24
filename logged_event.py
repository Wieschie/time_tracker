import datetime

class event(object):
    
    def __init__(self, type):
        self.datetime = datetime.datetime.utcnow().isoformat()
        self.type = type
        # no tags for now
        #self.tag = tag
    
    def __str__(self):
        return self.datetime + ", " + self.type
