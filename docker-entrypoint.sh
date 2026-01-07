PORT=${PORT:-8000}

echo "🚀 Starte Uvicorn sofort auf Port $PORT..."
python -m uvicorn --host 0.0.0.0 --port $PORT PatientPortal.asgi:application &
UVICORN_PID=$!

echo "⏳ Warte auf Azure SQL..."
python wait_for_db.py

echo "✅ DB bereit, führe Migrations durch..."
python manage.py migrate --noinput

# Wait for Uvicorn to exit
wait $UVICORN_PID
EXIT_CODE=$?

if [ "$EXIT_CODE" -ne 0 ]; then
    echo "⚠️ Uvicorn exited mit Code $EXIT_CODE, sende Fehlerbericht..."
    python - <<EOF
from PatientPortalApp.error_notifier import sendError
sendError(Exception("Uvicorn exited mit Code $EXIT_CODE"))
EOF
fi

exit "$EXIT_CODE"
