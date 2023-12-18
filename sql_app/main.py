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


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})


@app.get("/base", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(),  # optionally include the errors
                                  "body": exc.body,
                                  "custom msg": {"Your error message"}}),
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependence = Annotated[Session, Depends(get_db)]


# Запрос на создание пользователя
@app.post("/create_table/")
async def create_db(datum: DatumBase, db: db_dependence):
    db_obj = models.Datum(table_id=datum.table_id, table_datum=datum.table_datum)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)


# Запрос на удаление пользователя
@app.post("/delete_inqusitor/{table_id}")
async def create_db(table_id: int, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    db.delete(db_answer)
    db.commit()
    return db_answer


# Запрос на пользователя по id
@app.get("/get_inqusitor/{table_id}")
async def get_inqusitor(table_id: int, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="User is not exist")
    return db_answer


@app.get("/")
async def hello():
    return {"Hello", "World!"}
