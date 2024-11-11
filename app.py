#Подсказки 
#pip instal fastapi, pip install uvicorn
#uvicorn app:app --m reload

import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return "Привет мир!"
