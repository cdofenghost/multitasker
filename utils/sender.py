import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .secret_data import SENDER_EMAIL, SENDER_PASSWORD

def get_smtp_server(email: str) -> tuple[str, int]:
    smtp_pattern = "smtp."
    domain_name = email.split("@")[1]

    return (smtp_pattern + domain_name, 587)


def send_restoring_mail(receiver_email: str):
    server, port = get_smtp_server(SENDER_EMAIL)

    subject = "Восстановление доступа"
    body = "Привет, вот письмо о восстановлении аккаунта"

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    print(server, port, SENDER_EMAIL, receiver_email, SENDER_PASSWORD)
    try:
        with smtplib.SMTP(server, port) as host:
            host.starttls()
            host.login(SENDER_EMAIL, SENDER_PASSWORD)
            host.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        print("Письмо успешно отправлено")

    except Exception as e:
        print(f"Ошибка при отправлении письма: {e}")

send_restoring_mail("dofenspot@gmail.com")