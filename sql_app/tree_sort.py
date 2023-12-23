from typing import Annotated
import models
from schemas import InqusitorBase
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session

from fastapi import FastAPI, Body, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from pages.router import router as router_pages

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(router_pages)


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
@app.post("/create_db/")
async def create_db(inqusitor: InqusitorBase, db: db_dependence):
    db_obj = models.Inqusitor(inqusitor_id=inqusitor.inqusitor_id, inqusitor_name=inqusitor.inqusitor_name,
                              inqusitor_pass=inqusitor.inqusitor_pass)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)


# Запрос на удаление пользователя
@app.post("/delete_inqusitor/{inqusitor_id}")
async def create_db(inqusitor_id: int, db: db_dependence):
    db_answer = db.query(models.Inqusitor).filter(models.Inqusitor.inqusitor_id == inqusitor_id).first()
    db.delete(db_answer)
    db.commit()
    return db_answer


# Запрос на пользователя по id
@app.get("/get_inqusitor/{inqusitor_id}")
async def get_inqusitor(inqusitor_id: int, db: db_dependence):
    db_answer = db.query(models.Inqusitor).filter(models.Inqusitor.inqusitor_id == inqusitor_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="User is not exist")
    return db_answer


@app.get("/")
async def hello():
    return {"Hello", "World!"}
