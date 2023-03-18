import mysql.connector

class WebhookMySql:
    def __init__(self, cnx):
        self.cnx = cnx

    def create_webhook(self, webhook, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor()
            add_webhook = ("INSERT INTO webhooks "
                           "(uid, endpoint, event_type, secret_key, enabled) "
                           "VALUES (%s, %s, %s, %s, %s)")
            data_webhook = (webhook.uid, webhook.endpoint, webhook.event_type, webhook.secret_key, webhook.enabled)
            cursor.execute(add_webhook, data_webhook)
            if not transaction:
                self.cnx.commit()
        except:
            if not transaction:
                self.cnx.rollback()
            raise

    def read_webhook(self, uid, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor(dictionary=True)
            query = ("SELECT * FROM webhooks WHERE uid=%s")
            cursor.execute(query, (uid,))
            row = cursor.fetchone()
            if row is None:
                return None
            else:
                return Webhook(**row)
        except:
            raise

    def update_webhook(self, webhook, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor()
            update_webhook = ("UPDATE webhooks SET endpoint=%s, event_type=%s, "
                              "secret_key=%s, enabled=%s, updated_at=NOW() WHERE uid=%s")
            data_webhook = (webhook.endpoint, webhook.event_type, webhook.secret_key, webhook.enabled, webhook.uid)
            cursor.execute(update_webhook, data_webhook)
            if not transaction:
                self.cnx.commit()
        except:
            if not transaction:
                self.cnx.rollback()
            raise

    def delete_webhook(self, uid, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor()
            delete_webhook = ("DELETE FROM webhooks WHERE uid=%s")
            cursor.execute(delete_webhook, (uid,))
            if not transaction:
                self.cnx.commit()
        except:
            if not transaction:
                self.cnx.rollback()
            raise

    def get_all_webhooks(self, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor(dictionary=True)
            query = ("SELECT * FROM webhooks")
            cursor.execute(query)
            rows = cursor.fetchall()
            webhooks = []
            for row in rows:
                webhook = Webhook(**row)
                webhooks.append(webhook)
            return webhooks
        except:
            raise
