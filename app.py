#Подсказки 
#pip install fastapi, pip install uvicorn
#uvicorn app:app --m reload

import datetime
from fastapi import FastAPI
from pydantic import BaseModel

class Order(BaseModel):
    number : int
    startDate : datetime.date
    device : str
    problemType : str
    description : str
    client : str
    status : str

repo = []

app = FastAPI()

@app.get("/")
def read_root():
    return "Привет мир!"
