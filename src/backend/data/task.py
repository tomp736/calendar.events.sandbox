class Task:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.title = kwargs.get('title', None)
        self.description = kwargs.get('description', None)
        self.duration = kwargs.get('duration', None)
        self.completed = kwargs.get('completed', False)
        self.created_at = kwargs.get('created_at', None)
        self.updated_at = kwargs.get('updated_at', None)