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
    
    
def send_hello_email(recipient):
    print(smtp_server)
    print(smtp_port)
    print(username)
    print(password)
    msg = MIMEText("Hello, World!")
    msg["Subject"] = "Test Email"
    msg["From"] = username
    msg["To"] = recipient


    try:
        if smtp_port == 465:
            # SSL connection
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(username, password)
                server.send_message(msg)
        else:
            # TLS connection
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print("❌ Error sending email:", e)
        return False