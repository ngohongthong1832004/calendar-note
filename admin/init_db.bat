@echo off
del /F db.sqlite3
del calendarSite\migrations\0001_initial.py

call python manage.py makemigrations

call python manage.py migrate

call python init_db.py

rmdir /s /q calendarSite\migrations\__pycache__
rmdir /s /q calendarSite\__pycache__
rmdir /s /q calendarSite\__pycache__


call python manage.py runserver