from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException

import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Annotated
from database import db_dependence

router = APIRouter(
    prefix="/CRUD",
    tags=["CRUD"]
)


@router.get("/Get")
def ddd():
    return {"Hello ": "World"}


# Запрос для вывода всех таблиц
@router.get("/")
async def get_all_tables(request: Request, db: db_dependence, offset: int = 0, limit: int = 20):
    db_answer = db.query(models.Datum).offset(offset).limit(limit).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return db_answer

