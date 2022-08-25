pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
> http://localhost:8000/api/sword
