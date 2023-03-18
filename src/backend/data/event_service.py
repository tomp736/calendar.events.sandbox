
class EventService:
    def __init__(self, dao):
        self.dao = dao

    def create_event(self, event):
        self.dao.create_event(event)

    def read_event(self, uid):
        return self.dao.read_event(uid)

    def update_event(self, event):
        self.dao.update_event(event)

    def delete_event(self, uid):
        self.dao.delete_event(uid)

    def get_all_events(self):
        return self.dao.get_all_events()