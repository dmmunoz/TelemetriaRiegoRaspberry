import socket

def hay_internet(timeout=3):
    """
    Comprueba si hay salida a Internet.
    Devuelve True si hay conexión y False si no.
    """
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False

def enviar_correo(asunto, mensaje):
    """
    Envía un correo. Si no hay Internet o falla el servidor SMTP,
    devuelve False sin bloquear el sistema.
    """

    if not hay_internet():
        print("Correo no enviado: sin conexión a Internet")
        return False

    try:
        msg = MIMEMultipart()

        msg["From"] = formataddr(
            (EMAIL_NOMBRE_REMITENTE, EMAIL_REMITENTE)
        )

        msg["To"] = ", ".join(EMAIL_DESTINATARIOS)
        msg["Subject"] = asunto

        msg.attach(MIMEText(mensaje, "plain", "utf-8"))

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
        print(f"Correo no enviado: {e}")
        return False
