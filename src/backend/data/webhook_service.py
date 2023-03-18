
class WebhookService:
    
    def __init__(self, dao):
        self.dao = dao

    def create_webhook(self, webhook):
        self.dao.create_webhook(webhook)

    def read_webhook(self, uid):
        return self.dao.read_webhook(uid)

    def update_webhook(self, webhook):
        self.dao.update_webhook(webhook)

    def delete_webhook(self, uid):
        self.dao.delete_webhook(uid)

    def get_all_webhooks(self):
        return self.dao.get_all_webhooks()