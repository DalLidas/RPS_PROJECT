import models
from database import engine, db_dependence

from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from CRUD import router as crud_router, get_all_tables

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(crud_router)


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
async def table_selector(request: Request, data=Depends(get_all_tables)):
    if not data:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return templates.TemplateResponse("home.html", {"request": request, "tables": data})


# Проверка на пустой фильтр
@app.get("/table_filter", response_class=HTMLResponse)
async def table_filter(request: Request, db: db_dependence):
    return RedirectResponse("/table_selector")


# Вывод главной страницы c фильтром
@app.get("/table_filter/{table_name}", response_class=HTMLResponse)
async def table_filter(table_name: str, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).offset(0).limit(20).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return templates.TemplateResponse("home.html", {"request": request, "tables": db_answer, "filter": table_name})


# Проверка на пустой игнор-фильтр
@app.get("/table_ignore_filter", response_class=HTMLResponse)
async def table_ignore_filter(request: Request, db: db_dependence):
    return RedirectResponse("/table_selector")


# Вывод главной страницы c игнор-фильтром
@app.get("/table_ignore_filter/{table_name}", response_class=HTMLResponse)
async def table_ignore_filter(table_name: str, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name != table_name).offset(0).limit(20).all()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return templates.TemplateResponse("home.html", {"request": request, "tables": db_answer, "ignore_filter": table_name})


# Вывод страницы для редоктирования таблицы
@app.get("/table_editor/{table_id}", response_class=HTMLResponse)
async def table_editor(table_id: int, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return templates.TemplateResponse("edit.html", {"request": request, "table": db_answer})


# Создаёт пустые таблицы + вывод начальной страницы
@app.get("/table_creator/{table_name}", response_class=HTMLResponse)
async def table_creator(table_name: str, request: Request, db: db_dependence):
    db_answer = models.Datum(table_name=table_name, table_datum={"0": [], '1': []})
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)

    if not db_answer:
        raise HTTPException(status_code=404, detail="Data base doesn't have any table")
    return RedirectResponse("/table_selector")


# Удаление всех таблиц по имени + вывод начальной страницы
@app.delete("/table_remover_by_name/{table_name}", response_class=HTMLResponse)
async def table_remover(table_name: str, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).first()
    while db_answer:
        db.delete(db_answer)
        db.commit()
        db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).first()

    return RedirectResponse("/table_selector")


# Удаление таблицы по id + вывод начальной страницы
@app.delete("/table_remover_by_id/{table_id}", response_class=HTMLResponse)
async def table_remover(table_id: int, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    db.delete(db_answer)
    db.commit()

    return RedirectResponse("/table_selector")


# Сортировка таблицы + вывод начальной страницы
@app.put("/table_sorter/{table_id}", response_class=HTMLResponse)
async def table_sorter(table_id: int, request: Request, db: db_dependence):
    db_answer = db.query(models.Datum).filter(models.Datum.table_id == table_id).first()
    return db_answer
