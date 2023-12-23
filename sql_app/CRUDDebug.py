import random

from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

import models
from database import db_dependence

router = APIRouter(
    prefix="/CRUDDebug",
    tags=["CRUDDebug"]
)


# Создаёт случайно заполненные таблицы
@router.post("/create_table/{table_name}")
async def create_random_table(table_name: str, table_number: int, request: Request, db: db_dependence):
    db_answer = models.Datum()
    for _ in range(table_number):
        db_answer = models.Datum(table_name=table_name, table_datum={"0": [round(random.uniform(-10, 10), 2) for _ in range(random.randrange(2, 20))], '1': []})
        db.add(db_answer)

    db.commit()
    db.refresh(db_answer)

    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return {"status_code": 200, "db_answer": db_answer}


# Создаёт пустые таблицы + вывод начальной страницы
@router.post("/sort_table/{table_name}")
async def sort_many_table(table_name: str, table_number: int, request: Request, db: db_dependence):
    db_answers = db.query(models.Datum).filter(models.Datum.table_id == table_name).limit(table_number).all()
    for db_answer in db_answers:
        data = jsonable_encoder(db_answer.table_datum)
        data["1"] = sorted(data["0"])

        db_answer.sort_flag = True
        db_answer.table_datum = data

        db.commit()
        db.refresh(db_answer)

    return {"status_code": 200, "db_answer": db_answers}


# Создаёт пустые таблицы + вывод начальной страницы
@router.delete("/delete_table/{table_name}")
async def delete_table(table_name: str, table_number: int, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).limit(table_number).all()

    db.delete(db_answer)
    db.commit()

    return {"status_code": 200, "db_answer": db_answer}