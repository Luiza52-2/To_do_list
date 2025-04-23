import sqlite3
from datetime import datetime
from db import queries
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASKS)
    conn.commit()
    conn.close()


def get_tasks(sort_by="created_at DESC"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.SELECT_TASKS.format(sort_by))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def add_task_db(task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(queries.INSERT_TASK, (task, created_at))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id


def update_task_db(task_id, new_task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_TASK, (new_task, task_id))
    conn.commit()
    conn.close()


def toggle_task_status(task_id, is_done):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.TOGGLE_TASK_STATUS, (is_done, task_id))
    conn.commit()
    conn.close()


def delete_task_db(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()

def delete_completed_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_COMPLETED_TASKS)
    conn.commit()
    conn.close()