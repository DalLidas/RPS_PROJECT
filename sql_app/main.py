from typing import Annotated
import models
from schemas import DatumBase
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session

from fastapi import FastAPI, Body, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependence = Annotated[Session, Depends(get_db)]


async def get_table_all1(db: db_dependence, limit: int = 20, offset: int = 0):
    db_answer = db.query(models.Datum).offset(offset).limit(limit).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return db_answer


# Запрос на все таблицы
@app.get("/get_table_all/{limit, offset}")
async def get_table_all(db: db_dependence, limit: int = 20, offset: int = 0):
    db_answer = db.query(models.Datum).offset(offset).limit(limit).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return db_answer


# Запрос на таблицу по имени
@app.get("/get_table_name/{table_name}")
async def get_table_by_name(table_name: str, db: db_dependence, limit: int = 1, offset: int = 0):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).offset(offset).limit(limit).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Table(s) with this name is not exist")
    return db_answer


# Запрос на таблицу по id
@app.get("/get_table_id/{table_id}")
async def get_table_by_id(table_id: int, db: db_dependence, limit: int = 1, offset: int = 0):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).offset(offset).limit(limit).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Table(s) with this id is not exist")
    return db_answer


# Запрос на создание таблицы
@app.post("/create_table/")
async def create_table(datum: DatumBase, db: db_dependence):
    db_answer = models.Datum(table_name=datum.table_name, table_datum=datum.table_datum)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


# Запрос на удаление пользователя
@app.post("/delete_table/{table_id}")
async def delete_table(table_id: int, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    db.delete(db_answer)
    db.commit()
    return db_answer


# Разширенная обработка ошибок валидации данных
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(),  # optionally include the errors
                                  "body": exc.body,
                                  "custom msg": {"Your error message"}}),
    )


# Вывод главной страницы
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):  # , db=Depends(Annotated[Session, Depends(get_db)])
    return templates.TemplateResponse("base.html", {"request": request, "tables": ["Hello", "World", "Im", "Friendly"]})
