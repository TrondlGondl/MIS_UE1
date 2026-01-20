import os, time, pyodbc
from dotenv import load_dotenv
from PatientPortalApp.error_notifier import sendError

load_dotenv()

required_vars = ["AZURE_SQL_HOST", "AZURE_SQL_DATABASE", "AZURE_SQL_USER", "AZURE_SQL_PASSWORD"]
for var in required_vars:
    if not os.getenv(var):
        e = ValueError(f"Environment variable {var} is missing!")
        sendError(e)
        raise e

conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{os.getenv('AZURE_SQL_HOST')},1433;"
    f"Database={os.getenv('AZURE_SQL_DATABASE')};"
    f"Uid={os.getenv('AZURE_SQL_USER')};"
    f"Pwd={os.getenv('AZURE_SQL_PASSWORD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

deadline = time.time() + 120  # z.B. 2 Minuten

while True:
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        print("✅ Azure SQL läuft")
        break
    except Exception as e:
        print(f"⏳ Azure SQL noch nicht erreichbar... ({e})")
        if time.time() > deadline:
            sendError(e)
            raise SystemExit(1)
        time.sleep(5)
