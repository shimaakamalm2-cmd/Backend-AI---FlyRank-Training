from ast import List


from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    done: bool

# in memory or hardcode examples and outside of the class
tasks: list[Task]= [
        Task(id=1, title="Buy groceries", done=False),
        Task(id=2, title="Walk the dog", done=True),
        Task(id=3, title="Finish backend stage 2", done=False),
    ]

@app.get("/tasks")
def read_tasks():
    return tasks
#f means formatted string so its not took as literal string 
@app.get("/tasks/{id}")
def read_task(id: int):
    if id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {id} not found")
    return tasks[id]

