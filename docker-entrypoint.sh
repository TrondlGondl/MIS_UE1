sleep 2
python manage.py makemigrations
python manage.py migrate
python -m uvicorn --host 0.0.0.0 --port 8000 PatientPortal.asgi:application