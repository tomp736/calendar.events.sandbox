from data.task import Task
import mysql.connector

class TaskMySql:
    def __init__(self, cnx):
        self.cnx = cnx

    def create_task(self, task, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor()
            add_task = ("INSERT INTO tasks "
                        "(title, description, duration, completed) "
                        "VALUES (%s, %s, %s, %s)")
            data_task = (task.title, task.description, task.duration, task.completed)
            cursor.execute(add_task, data_task)
            if not transaction:
                self.cnx.commit()
        except:
            if not transaction:
                self.cnx.rollback()
            raise

    def read_task(self, task_id, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor(dictionary=True)
            query = ("SELECT * FROM tasks WHERE id=%s")
            cursor.execute(query, (task_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            else:
                return Task(**row)
        except:
            raise

    def update_task(self, task, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor()
            update_task = ("UPDATE tasks SET title=%s, description=%s, duration=%s, completed=%s, updated_at=NOW() WHERE id=%s")
            data_task = (task.title, task.description, task.duration, task.completed, task.id)
            cursor.execute(update_task, data_task)
            if not transaction:
                self.cnx.commit()
        except:
            if not transaction:
                self.cnx.rollback()
            raise

    def delete_task(self, task_id, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor()
            delete_task = ("DELETE FROM tasks WHERE id=%s")
            cursor.execute(delete_task, (task_id,))
            if not transaction:
                self.cnx.commit()
        except:
            if not transaction:
                self.cnx.rollback()
            raise

    def get_all_tasks(self, transaction=None):
        try:
            cursor = transaction.cursor() if transaction else self.cnx.cursor(dictionary=True)
            query = ("SELECT * FROM tasks")
            cursor.execute(query)
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                task = Task(**row)
                tasks.append(task)
            return tasks
        except:
            raise