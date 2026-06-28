import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from config_email import (
    SMTP_SERVIDOR,
    SMTP_PUERTO,
    EMAIL_REMITENTE,
    EMAIL_NOMBRE_REMITENTE,
    EMAIL_PASSWORD,
    EMAIL_DESTINATARIOS,
)


def hay_internet(timeout=3):
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False


def enviar_correo(asunto, mensaje):
    """
    Envía correo solo si hay conexión.
    Si no hay Internet o falla SMTP, no bloquea el sistema.
    Devuelve True si se envía, False si no.
    """

    if not hay_internet():
        print("Correo no enviado: sin conexión a Internet")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = formataddr((EMAIL_NOMBRE_REMITENTE, EMAIL_REMITENTE))
        msg["To"] = ", ".join(EMAIL_DESTINATARIOS)
        msg["Subject"] = asunto

        msg.attach(MIMEText(mensaje, "plain", "utf-8"))

        with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PUERTO, timeout=10) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
            servidor.send_message(msg)

        print(f"Correo enviado: {asunto}")
        return True

    except Exception as e:
        print(f"Correo no enviado por error: {e}")
        return False
