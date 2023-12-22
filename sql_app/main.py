import models
from schemas import DatumBase
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated

from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
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
@app.get("/table_selector", response_class=HTMLResponse)
async def home(request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).offset(0).limit(20).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return templates.TemplateResponse("home.html", {"request": request, "tables": db_answer})


# Проверка на пустой фильтр
@app.get("/table_filter", response_class=HTMLResponse)
async def home(request: Request, db: db_dependence):
    return RedirectResponse("/table_selector")


# Вывод главной страницы c фильтром
@app.get("/table_filter/{table_name}", response_class=HTMLResponse)
async def home(table_name: str, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).offset(0).limit(20).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return templates.TemplateResponse("home.html", {"request": request, "tables": db_answer, "filter": table_name})


# Проверка на пустой игнор-фильтр
@app.get("/table_ignore_filter", response_class=HTMLResponse)
async def home(request: Request, db: db_dependence):
    return RedirectResponse("/table_selector")


# Вывод главной страницы c игнор-фильтром
@app.get("/table_ignore_filter/{table_name}", response_class=HTMLResponse)
async def home(table_name: str, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name != table_name).offset(0).limit(20).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return templates.TemplateResponse("home.html", {"request": request, "tables": db_answer, "ignore_filter": table_name})


# Вывод страницы для редоктирования таблицы
@app.get("/table_editor/{table_id}", response_class=HTMLResponse)
async def home(table_id: int, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return templates.TemplateResponse("edit.html", {"request": request, "table": db_answer})


# Создаёт пустые таблицы + вывод начальной страницы
@app.get("/table_creator/{table_name}", response_class=HTMLResponse)
async def home(table_name: str, request: Request, db: db_dependence):
    db_answer = models.Datum(table_name=table_name, table_datum={"0": 0, '1': 0})
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)

    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return RedirectResponse("/table_selector")


# Удаление всех таблиц по имени + вывод начальной страницы
@app.get("/table_remover/{table_name}", response_class=HTMLResponse)
async def home(table_name: str, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).first()
    while db_answer:
        db.delete(db_answer)
        db.commit()
        db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).first()

    return RedirectResponse("/table_selector")
