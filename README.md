#Я запускал под IDE PyCharm
#Для работы необходимо установить некоторые библеотеки с помощью команды:

$pip install fastapi[all] uvicorn sqlalchemy psycopg2-binary

#Для запуска необходимо написать команды в консоль

$cd sql_app
$uvicorn main:app --reload

