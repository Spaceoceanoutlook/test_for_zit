# test_for_zit

Тестовое задание

## **Запуск**

- git clone https://github.com/Spaceoceanoutlook/test_for_zit.git
- poetry install (Установка библиотек)
- poetry shell (Активировать виртуальное окружение)
- cd .\test_for_zit\ 
- в root directory создать файл .env, прописать в нем: <br/>
DB_NAME = "придумайте имя базы данных" <br/>
USER = "ваш логин от Postgresql" <br/>
PASSWORD = "ваш пароль от Postgresql" <br/>
- alembic upgrade head (Создание таблиц в БД)
- main.py
