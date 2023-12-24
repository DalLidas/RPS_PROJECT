from fastapi.encoders import jsonable_encoder
from database import db_dependence, SessionLocal
import models
import random
import time


# Создание случайно заполненых таблиц
def create_random_table(table_name: str, table_number: int, db: db_dependence):
    db_answer = models.Datum()
    start_time = time.time()

    try:
        for _ in range(table_number):
            db_answer = models.Datum(table_name=table_name, table_datum={
                "0": [round(random.uniform(-10, 10), 2) for _ in range(random.randrange(2, 20))], '1': []})
            db.add(db_answer)
            db.commit()

    except:
        return [False, time.time() - start_time]

    return [True, time.time() - start_time]


# Сортировка случайных таблиц
def sort_table(table_name: str, table_number: int, db: db_dependence):
    start_time = time.time()
    try:
        db_answers = db.query(models.Datum).filter(models.Datum.table_name == table_name and not models.Datum.sort_flag).limit(table_number).all()
        for db_answer in db_answers:
            data = jsonable_encoder(db_answer.table_datum)
            data["1"] = sorted(data["0"])

            db_answer.sort_flag = True
            db_answer.table_datum = data
            db.commit()
            db.refresh(db_answer)

    except:
        return [False, time.time() - start_time]

    return [True, time.time() - start_time]


# Удаление случайных таблиц
def delete_table(table_name: str, table_number: int, db: db_dependence):
    start_time = time.time()
    try:
        for _ in range(table_number):
            db_answer = db.query(models.Datum).filter(models.Datum.table_name == table_name).limit(table_number).first()

            db.delete(db_answer)
            db.commit()

    except:
        return [False, time.time() - start_time]

    return [True, time.time() - start_time]


# Вывод метрик
def metrics_handler(metrica: list[bool, float], stat: dict, msg: str):
    if metrica[0]:
        print(f"{msg} was PASS! Execution time: {round(metrica[1], 4)} seconds")
        stat["test_passed"] += 1
        stat["execution_time"] += round(metrica[1], 4)
    else:
        print(f"{msg} was FAIL! Execution time: {round(metrica[1], 4)} seconds")
        stat["execution_time"] += round(metrica[1], 4)


if input("Выполнить юнит-тестирования (Y/N)") == "Y":
    session = SessionLocal()
    create_stat = {"test_passed": 0, "execution_time": 0}
    sort_stat = {"test_passed": 0, "execution_time": 0}
    delete_stat = {"test_passed": 0, "execution_time": 0}

    print("===============================================================")
    metrics_handler(create_random_table("Tester", 100, session), create_stat, "Create 100 table test")
    metrics_handler(create_random_table("Tester", 1000, session), create_stat, "Create 1000 table test")
    metrics_handler(create_random_table("Tester", 10000, session), create_stat, "Create 10000 table test")
    print("---------------------------------------------------------------")
    metrics_handler(sort_table("Tester", 100, session), sort_stat, "Sort 100 table test")
    metrics_handler(sort_table("Tester", 1000, session), sort_stat, "Sort 1000 table test")
    metrics_handler(sort_table("Tester", 10000, session), sort_stat, "Sort 10000 table test")
    print("---------------------------------------------------------------")
    metrics_handler(delete_table("Tester", 100, session), delete_stat, "Delete 100 table test")
    metrics_handler(delete_table("Tester", 1000, session), delete_stat, "Delete 1000 table test")
    metrics_handler(delete_table("Tester", 10000, session), delete_stat, "Delete 10000 table test")
    print("===============================================================")
    print("                     Group Totals")
    print("===============================================================")
    print(f"Create tests passed: {create_stat['test_passed']} / 3")
    print(f"Create tests execution time: {round(create_stat['execution_time'], 4)} seconds")
    print("---------------------------------------------------------------")
    print(f"Sort tests passed: {sort_stat['test_passed']} / 3")
    print(f"Sort tests execution time: {round(sort_stat['execution_time'], 4)} seconds")
    print(f"Sort tests average execution time: {round(sort_stat['execution_time'] / 11100, 4)} seconds")
    print("---------------------------------------------------------------")
    print(f"Delete tests passed: {delete_stat['test_passed']} / 3")
    print(f"Delete tests execution time: {round(delete_stat['execution_time'], 4)} seconds")
    print("===============================================================")
    print("                        Totals")
    print("===============================================================")
    print(f"Total tests passed: {create_stat['test_passed'] + sort_stat['test_passed'] + delete_stat['test_passed']} / 9")
    print(f"Total tests execution time: {round(create_stat['execution_time'] + sort_stat['execution_time'] + delete_stat['execution_time'], 4)} seconds")
    print("===============================================================")
