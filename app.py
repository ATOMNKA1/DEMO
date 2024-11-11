#Подсказки 
#pip install fastapi, pip install uvicorn
#uvicorn app:app --reload

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

repo = [
    Order(
        number = 1,
        startDate = "2024-11-11",
        device = "Телефон",
        problemType = "поломка экрана",
        description = "трещина",
        client = "Иван Иванович Иванов",
        status = "В обработке"
    )
]

app = FastAPI()

@app.get("/orders")
def get_orders():
    return repo
