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
    endDate : Optional[datetime.date] = None
    master : Optional[str] = "Не назначен"
    comments : Optional[list] = []

class UpdateOrderDTO(BaseModel):
    number : int
    status : Optional[str] = ""
    description : Optional[str] = ""
    master : Optional[str] = ""
    comment : Optional[str] = str

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
    buffer = message
    message = ""
    if(param):
        return {"repo": [ o for o in repo if o.number == int(param)], "message": buffer}

    return {"repo": repo, "message": buffer}

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
                if (o.status == "Выполнено"):
                    message += f"Заявка №{o.number} Завершена\n"
                    o.endDate = datetime.datetime.now()
            if dto.description != o.description and dto.description != "":
                o.description = dto.description
            if dto.master != o.master and dto.master != "":
                o.master = dto.master
            if dto.comment != None and dto.comment !="":
                o.comments.append(dto.comment)
            return 0
    return "Заявка не найдена"

def complete_count():
    a = [o for o in repo if o.status == "Выполнено"]
    return len(a)

def get_problem_type_stat():
    dict = {}
    for o in repo:
        if o.problemType in dict.keys():
            dict[o.problemType] += 1
        else:
            dict[o.problemType] = 1
    return dict

def get_average_time_to_complete():
    times = [(
        datetime.datetime(o.endDate.year, o.endDate.month, o.endDate.day)
        - datetime.datetime(o.startDate.year, o.startDate.month, o.startDate.day)).days
              for o in repo 
              if o.status == "Выполнено"]
    if complete_count() != 0:
        return sum(times)/complete_count()
    return 0
            
@app.get("/statistics")
def get_statistics():
    return {
        "complete_count" : complete_count(),
        "get_problem_type_stat" : get_problem_type_stat(),
        "get_average_time_to_complete" : get_average_time_to_complete()
    }