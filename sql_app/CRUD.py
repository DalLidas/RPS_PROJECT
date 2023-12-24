from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

import models
from database import db_dependence

#from sortings.tree_sort import tree_sort

router = APIRouter(
    prefix="/CRUD",
    tags=["CRUD"],
)


# читает из куки цветовую тему
@router.get("/get_visual_mod")
def get_visual_mod(request: Request):
    return request.cookies.get('visual_mod')


# Запрос для вывода всех таблиц
@router.get("/get_tables")
async def get_tables(request: Request, db: db_dependence, offset: int = 0, limit: int = 40):
    db_answer = db.query(models.Datum).offset(offset).limit(limit).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return {"status_code": 200, "db_answer": db_answer}


# # Запрос на вывод таблицы по name
@router.get("/get_table_by_name")
async def get_table_by_name(table_name: str, request: Request, db: db_dependence, offset: int = 0, limit: int = 40):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).offset(offset).limit(limit).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return {"status_code": 200, "db_answer": db_answer}


# Запрос на вывод таблицы по id
@router.get("/get_table_by_id")
async def get_table_by_id(table_id: int, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return {"status_code": 200, "db_answer": db_answer}


# Запрос для вывода таблиц по игнор фильтру
@router.get("/get_ignore_filtered_tables")
async def get_ignore_filtered_tables(table_name: str, request: Request, db: db_dependence, offset: int = 0, limit: int = 40):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name != table_name).offset(offset).limit(limit).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return {"status_code": 200, "db_answer": db_answer}


# Создаёт пустые таблицы + вывод начальной страницы
@router.post("/create_table/{table_name}")
async def create_table(table_name: str, request: Request, db: db_dependence):
    db_answer = models.Datum(table_name=table_name, table_datum={"0": [], '1': []})
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)

    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return {"status_code": 200, "db_answer": db_answer}


# Удаление всех таблиц по имени
@router.delete("/remove_table_by_name/{table_name}")
async def remove_table_by_name(table_name: str, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).first()
    while db_answer:
        db.delete(db_answer)
        db.commit()
        db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).first()

    return {"status_code": 200, "db_answer_last": db_answer}


# Удаление таблицы по id
@router.delete("/remove_table_by_id/{table_id}")
async def remove_table_by_id(table_id: int, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    db.delete(db_answer)
    db.commit()

    return {"status_code": 200, "db_answer_last": db_answer}


# Сортировка таблицы
@router.put("/sort_table/{table_id}")
async def sort_table(table_id: int, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    data = jsonable_encoder(db_answer.table_datum)
    #data["1"] = tree_sort(data["0"])

    db_answer.sort_flag = True
    db_answer.table_datum = data

    db.commit()
    db.refresh(db_answer)

    return {"status_code": 200, "db_answer": db_answer}


# Изменение таблицы
@router.put("/change_table/{table_id}")
async def change_table(table_id: int, table_name: str, data: list[float], request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    json_data = jsonable_encoder(db_answer.table_datum)
    json_data["0"] = jsonable_encoder(data)

    db_answer.table_name = table_name
    db_answer.sort_flag = False
    db_answer.table_datum = json_data

    db.commit()
    db.refresh(db_answer)

    return {"status_code": 200, "db_answer": db_answer}


