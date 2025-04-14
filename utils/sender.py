import smtplib
from random import randint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ..schemas.user import UserSchema
from .secret_data import SENDER_EMAIL, SENDER_PASSWORD

def get_smtp_server(email: str) -> tuple[str, int]:
    smtp_pattern = "smtp."
    domain_name = email.split("@")[1]

    return (smtp_pattern + domain_name, 587)

def generate_code() -> str:
    code = randint(0, 9999)
    return f"{code:04}"

def send_restoring_mail(receiver_email: str) -> str:
    server, port = get_smtp_server(SENDER_EMAIL)

    subject = "Восстановление доступа"
    code = generate_code()
    body = f"Привет, это письмо о восстановлении твоего аккаунта.<br></br><br>Код для восстановления: <b>{code}</b></br>"

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(server, port) as host:
            host.starttls()
            host.login(SENDER_EMAIL, SENDER_PASSWORD)
            host.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        print("Письмо успешно отправлено")

    except Exception as e:
        print(f"Ошибка при отправлении письма: {e}")

    return code

def send_invitation_mail(user: UserSchema, receiver_email: str):
    server, port = get_smtp_server(SENDER_EMAIL)

    subject = "Восстановление доступа"
    body = f"""
    Пользователь <b>{user.name}</b> хочет пригласить вас в проект в приложении MultiTasker, но вы еще не зарегистрированы!
    <br><a href="http://127.0.0.1:8000/app/register">Переходите по ссылке</a> и планируйте вместе!
    """

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(server, port) as host:
            host.starttls()
            host.login(SENDER_EMAIL, SENDER_PASSWORD)
            host.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        print("Письмо успешно отправлено")

    except Exception as e:
        print(f"Ошибка при отправлении письма: {e}")
