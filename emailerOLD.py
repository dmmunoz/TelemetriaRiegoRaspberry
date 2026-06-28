import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config_email import SMTP_SERVIDOR, SMTP_PUERTO, EMAIL_REMITENTE, EMAIL_PASSWORD, EMAIL_DESTINATARIOS


def enviar_correo(asunto, mensaje):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMITENTE
    msg["To"] = ", ".join(EMAIL_DESTINATARIOS)
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "plain", "utf-8"))

    with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PUERTO) as servidor:
        servidor.starttls()
        servidor.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
        servidor.send_message(msg)
