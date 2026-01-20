set -e

PORT=${PORT:-8000}

echo "⏳ Warte auf Azure SQL..."
python wait_for_db.py

echo "✅ DB bereit, führe Migrations durch..."
python manage.py migrate --noinput

echo "🚀 Starte Uvicorn auf Port $PORT..."
python -m uvicorn --host 0.0.0.0 --port $PORT PatientPortal.asgi:application
