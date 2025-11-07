import smtplib
from email.mime.text import MIMEText
from app.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

smtp_server = settings.SMTP_SERVER
smtp_port = settings.SMTP_PORT
username = settings.SMTP_USERNAME
password = settings.SMTP_PASSWORD


def send_email_with_attachment(recipient, subject, body, filepath):
    """
    Send an email with an attachment to a specified recipient.

    Args:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The body text of the email.
        filepath (str): The path to the file to attach.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = recipient

    body = MIMEText(body)
    msg.attach(body)

    with open(filepath, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(filepath))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(filepath)}"'
    msg.attach(part)

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(username, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
        return True
    except Exception as e:
        return False
