#!/bin/sh
set -e

echo "Warte auf Azure SQL..."
python wait_for_db.py

sleep 2
python manage.py makemigrations
python manage.py migrate

echo "Starte Django (uvicorn)..."
python -m uvicorn --host 0.0.0.0 --port 8000 PatientPortal.asgi:application
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
python - <<EOF
from PatientPortalApp.error_notifier import sendError
sendError(Exception("Uvicorn/Django exited mit Code $EXIT_CODE"))
EOF
fi

exit $EXIT_CODE
