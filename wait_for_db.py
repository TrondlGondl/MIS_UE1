import pyodbc
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Ensure environment variables exist
required_vars = ["AZURE_SQL_HOST", "AZURE_SQL_DATABASE", "AZURE_SQL_USER", "AZURE_SQL_PASSWORD"]
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Environment variable {var} is missing!")

conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{os.getenv('AZURE_SQL_HOST')},1433;"
    f"Database={os.getenv('AZURE_SQL_DATABASE')};"
    f"Uid={os.getenv('AZURE_SQL_USER')};"
    f"Pwd={os.getenv('AZURE_SQL_PASSWORD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

while True:
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        print("✅ Azure SQL läuft")
        break
    except pyodbc.Error as e:
        print(f"⏳ Azure SQL schläft noch... ({e})")
        time.sleep(5)
