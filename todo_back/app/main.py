from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session


app = FastAPI()
@app.get('/')
def root():
    return{"message":"hello"}

