#!/bin/sh
set -e

echo "⏳ Warte auf Azure SQL..."
python wait_for_db.py

echo "✅ DB bereit, starte Django..."

# Run migrations
python manage.py migrate --noinput

# Start Uvicorn
python -m uvicorn --host 0.0.0.0 --port 8000 PatientPortal.asgi:application
EXIT_CODE=$?

# If Uvicorn exited with an error, send notification
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "⚠️ Uvicorn exited mit Code $EXIT_CODE, sende Fehlerbericht..."
    python - <<EOF
from PatientPortalApp.error_notifier import sendError
sendError(Exception("Uvicorn exited mit Code $EXIT_CODE"))
EOF
fi

exit "$EXIT_CODE"
