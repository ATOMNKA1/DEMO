#Подсказки 
#pip install fastapi, pip install uvicorn, pip install python-multipart
#uvicorn app:app --reload

import datetime
from typing import Annotated, Optional
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class Order(BaseModel):
    number : int
    startDate : datetime.date
    device : str
    problemType : str
    description : str
    client : str
    status : str
    master : Optional[str] = "Не назначен"

class UpdateOrderDTO(BaseModel):
    number : int
    status : Optional[str] = ""
    description : Optional[str] = ""
    master : Optional[str] = ""

repo = [
    Order(
        number = 1,
        startDate = "2024-11-11",
        device = "Телефон",
        problemType = "поломка экрана",
        description = "трещина",
        client = "Иван Иванович Иванов",
        status = "В обработке"
    ),
    Order(
        number = 2,
        startDate = "2024-11-11",
        device = "Телефон",
        problemType = "поломка экрана",
        description = "трещина",
        client = "Иван Иванович Иванов",
        status = "В обработке"
    )
]

app = FastAPI()

message = ""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/orders")
def get_orders(param = None):
    global message
    if(param):
        return {"repo": [ o for o in repo if o.number == int(param)], "message": message}

    return {"repo": repo, "message": message}

@app.post("/orders")
def post_orders(dto : Annotated[Order, Form()]):
    repo.append(dto)

@app.post("/update")
def update_order(dto : Annotated[UpdateOrderDTO, Form()]):
    global message
    for o in repo:
        if o.number == dto.number:
            if dto.status != o.status and dto.status != "":
                o.status = dto.status
                message += f"Статус заявки №{o.number} изменён на: {dto.status} \n"
            if dto.description != o.description and dto.description != "":
                o.description = dto.description
            if dto.master != o.master and dto.master != "":
                o.master = dto.master
            return 0
    return "Заявка не найдена"