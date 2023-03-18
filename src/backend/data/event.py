class Event:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.uid = kwargs.get('uid', None)
        self.summary = kwargs.get('summary', None)
        self.description = kwargs.get('description', None)
        self.location = kwargs.get('location', None)
        self.start_time = kwargs.get('start_time', None)
        self.end_time = kwargs.get('end_time', None)
        self.created_at = kwargs.get('created_at', None)
        self.updated_at = kwargs.get('updated_at', None)