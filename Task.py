
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

@app.post("/tasks")
def create_task(task: TaskCreate):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)" , (task.title,))
    conn.commit()
    conn.close()


@app.patch("/tasks/{id}")
def update_task(id: int, task: TaskUpdate):
    conn = connect_db()
    cursor = conn.cursor()
    if not cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,)):
        conn.close()
        raise HTTPException(status_code=404, detail={"error": "Task not found"})

    #model dmp makes it a dict and the condition updates only the data sent in req
    update_task = task.model_dump(exclude_unset=True)

    # skip if used executed an empty update
    if update_task is None:
        conn.close()
        raise HTTPException(status_code=404, detail={"error": "no data to update"})

    #dynamic query clause to specify the chosen keys
    set_clause = " ,".join([f"{col} = ?" for col in update_task.keys()])
    # get the values of the keys to add them to the clause
    values = list(update_task.values())

    #executing the update clause with the dynamic query
    cursor.execute(f"UPDATE tasks SET {set_clause} WHERE id = {id}", values)
    conn.commit()
    conn.close()

@app.delete("/tasks/{id}")
def delete_task(id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()



