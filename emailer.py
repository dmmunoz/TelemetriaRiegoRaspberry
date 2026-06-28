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

    if not hay_internet():
        print("Sin conexión a Internet. No se envía el correo.")
        return False

    try:

        msg = MIMEMultipart()

        msg["From"] = formataddr(
            (EMAIL_NOMBRE_REMITENTE, EMAIL_REMITENTE)
        )

        msg["To"] = ", ".join(EMAIL_DESTINATARIOS)
        msg["Subject"] = asunto

        msg.attach(
            MIMEText(mensaje, "plain", "utf-8")
        )

        with smtplib.SMTP(
            SMTP_SERVIDOR,
            SMTP_PUERTO,
            timeout=10
        ) as servidor:

            servidor.ehlo()
            servidor.starttls()
            servidor.ehlo()

            servidor.login(
                EMAIL_REMITENTE,
                EMAIL_PASSWORD
            )

            servidor.send_message(msg)

        print("Correo enviado correctamente.")
        return True

    except Exception as e:

        print(f"Error enviando correo: {e}")
        return False
