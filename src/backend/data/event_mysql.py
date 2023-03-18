import mysql.connector
from data.event import Event

class EventMySql:
    def __init__(self, cnx):
        self.cnx = cnx

    def create_event(self, event, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor()
            add_event = ("INSERT INTO events "
                         "(uid, summary, description, location, start_time, end_time) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")
            data_event = (event.uid, event.summary, event.description, event.location, event.start_time, event.end_time)
            cursor.execute(add_event, data_event)
            if not transaction:
                self.cnx.commit()
        except:
            if not transaction:
                self.cnx.rollback()
            raise

    def read_event(self, uid, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor(dictionary=True)
            query = ("SELECT * FROM events WHERE uid=%s")
            cursor.execute(query, (uid,))
            row = cursor.fetchone()
            if row is None:
                return None
            else:
                return Event(**row)
        except:
            raise

    def update_event(self, event, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor()
            update_event = ("UPDATE events SET summary=%s, description=%s, location=%s, "
                            "start_time=%s, end_time=%s, updated_at=NOW() WHERE uid=%s")
            data_event = (event.summary, event.description, event.location, event.start_time, event.end_time, event.uid)
            cursor.execute(update_event, data_event)
            if not transaction:
                self.cnx.commit()
        except:
            if not transaction:
                self.cnx.rollback()
            raise

    def delete_event(self, uid, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor()
            delete_event = ("DELETE FROM events WHERE uid=%s")
            cursor.execute(delete_event, (uid,))
            if not transaction:
                self.cnx.commit()
        except:
            if not transaction:
                self.cnx.rollback()
            raise

    def get_all_events(self, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor(dictionary=True)
            query = ("SELECT * FROM events")
            cursor.execute(query)
            rows = cursor.fetchall()
            events = []
            for row in rows:
                event = Event(**row)
                events.append(event)
            return events
        except:
            raise
