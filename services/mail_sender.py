import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")

def send_email(
    recipient,
    subject,
    body,
    attachment_path
):
    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = recipient

    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        file_data = f.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=attachment_path.name
    )

    with smtplib.SMTP_SSL(
        SMTP_HOST,
        SMTP_PORT
    ) as smtp:
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
