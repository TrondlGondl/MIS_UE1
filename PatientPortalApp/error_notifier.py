import os
import smtplib
import traceback
from dotenv import load_dotenv

load_dotenv()

def sendError(e: Exception) -> None:
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    receiver = os.getenv("ERROR_RECEIVER")

    # Falls auf Azure nicht gesetzt -> sichtbar loggen
    if not all([smtp_server, smtp_port, smtp_user, smtp_password, receiver]):
        print("⚠️ sendError(): SMTP config missing. "
              "Check Azure App Settings (SMTP_SERVER/PORT/USER/PASSWORD/ERROR_RECEIVER).")
        return

    subject = f"Serverfehler: {e!r}"

    stacktrace = "".join(traceback.format_exception(type(e), e, e.__traceback__))

    body = f"""Ein Fehler ist aufgetreten.

Fehlermeldung:
{e!r}

Stacktrace:
{stacktrace}
"""

    message = f"""From: {smtp_user}
To: {receiver}
Subject: {subject}

{body}
"""

    try:
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, receiver, message)
            print("✅ Fehler-Mail gesendet an", receiver)
    except Exception as mail_error:
        print("❌ Fehler beim Senden der Fehler-Mail:", mail_error)
