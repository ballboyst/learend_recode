from database import get_db
from fastapi import FastAPI, Depends
from models import Users, Tasks
from schema import CreateTask
from sqlalchemy.orm import Session


app = FastAPI()


@app.get('/')
def root():
    return {"message": "hello"}


@app.post('/tasks')
def create_tasks(task: CreateTask, db: Session = Depends(get_db)):
    db_task = Tasks(
        title=task.title,
        description=task.description,
        done=False,
        uid=1, 
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return {"message": "Task received!"}


@app.get('/tasks')
def get_tasks(db: Session = Depends(get_db)):
    task_list = []
    tasks = db.query(Tasks).all()
    for task in tasks:
        task_list.append(task)
    
    return task_list
