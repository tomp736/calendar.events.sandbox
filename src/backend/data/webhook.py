class Webhook:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.uid = kwargs.get('uid', None)
        self.endpoint = kwargs.get('endpoint', None)
        self.event_type = kwargs.get('event_type', None)
        self.secret_key = kwargs.get('secret_key', None)
        self.enabled = kwargs.get('enabled', None)
        self.created_at = kwargs.get('created_at', None)
        self.updated_at = kwargs.get('updated_at', None)
