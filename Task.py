
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status

app = FastAPI()

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

#can not make a global connection , connection per request
# cause thread crash cuz fastapi handles requests using multithreading

#function for requesting connection
def connect_db():
    conn = sqlite3.connect("tasks.db")
    # Allows accessing columns by name like dicts: row["title"]
    #also fastapi seializes data into json , and dictionaries map directly to json
    conn.row_factory = sqlite3.Row
    return conn

class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool





@app.get("/tasks")
def read_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    tasks = cursor.fetchall()
    return tasks

@app.get("/tasks/{id}")
def read_task(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    task = cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    task = cursor.fetchone()  # fetch one row where id matches
    conn.close()
    if task is None:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})

    return task

