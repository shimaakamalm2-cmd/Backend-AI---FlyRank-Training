from ast import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool


# in memory or hardcode examples and outside of the class
tasks: list[Task] = [
    Task(id=1, title="Buy groceries", done=False),
    Task(id=2, title="Walk the dog", done=True),
    Task(id=3, title="Finish backend stage 2", done=False),
]


@app.get("/tasks")
def read_tasks():
    return tasks


#f means formatted string so it's not took as literal string
@app.get("/tasks/{id}")
def read_task(id: int):
    task= next((t for t in tasks if t.id == id), None)
    # or next_id= len(tasks) +1
    if not task:
        raise HTTPException(status_code=404, detail=f"Task{id} not found")
    return task

@app.post("/tasks")
def create_task(taskData: TaskCreate):
    if not taskData.title:
        raise HTTPException(status_code=400, detail="Task title cannot be blank")
    next_id = len(tasks)+1
    task =Task(id=next_id, title=taskData.title , done=False)
    tasks.append(task)
    return task
#can do custom validation in pydantic and also has build in validations
#can also convert to and from json easily
@app.put("/tasks/{id}")
def update_task(id: int, taskData: TaskUpdate):
    task= next((t for t in tasks if t.id == id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task{id} not found")
    task.title = taskData.title
    task.done = taskData.done
    return task
@app.delete("/tasks/{id}")
def delete_task(id: int):
    task= next((t for t in tasks if t.id == id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task{id} not found")
    tasks.remove(task)
