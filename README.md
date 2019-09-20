# Тестовое задание для Azur Games
____
__Установка проекта (bold)__

:black_square_button: virtualenv venv

:black_square_button: venv\scripts\activate

:black_square_button: pip install -r requirements.txt

:black_square_button: set FLASK_APP=page.py

:black_square_button: flask db migrate

:black_square_button: flask db upgrade

:black_square_button: flask run
____

Сервер запустится на http://localhost:5000/

Основной функционал находится по адресу /

Для заполнения таблицы тестовыми данными можно использовать __python script.py (bold)__ в консоли

Также на адрес /script можно передать параметр keyword GET запросом
____

Используется база данных SQLite 3
