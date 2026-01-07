import smtplib
import os
import traceback
from dotenv import load_dotenv

load_dotenv()


def sendError(e: Exception) -> None:
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    receiver = os.getenv("ERROR_RECEIVER")

    subject = f"Serverfehler: {str(e)}"
    stacktrace = traceback.format_exc()

    body = f"""
Ein Fehler ist aufgetreten.

Fehlermeldung:
{str(e)}

Stacktrace:
{stacktrace}
"""

    message = f"""From: {smtp_user}
To: {receiver}
Subject: {subject}

{body}
"""

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, receiver, message)
    except Exception as mail_error:
        print("Fehler beim Senden der Fehler-Mail:", mail_error)
