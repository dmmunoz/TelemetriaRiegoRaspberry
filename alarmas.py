from datetime import datetime

from database import (
    obtener_alarma_activa,
    crear_alarma_bd,
    marcar_correo_alarma_enviado,
    resolver_alarma_bd,
    registrar_evento,
)
from emailer import enviar_correo


def crear_alarma(nivel, codigo, titulo, descripcion):
    """
    Crea una alarma solo si no existe ya activa.
    Envía correo una sola vez.
    """

    alarma = obtener_alarma_activa(codigo)

    if alarma:
        return False

    crear_alarma_bd(nivel, codigo, titulo, descripcion)
    registrar_evento("ALARMA", nivel, titulo)

    asunto = f"[{nivel}] {titulo}"

    mensaje = f"""
CONTROL DE MANTENIMIENTO DE RIEGO DE SANTA FE

{titulo}

Nivel: {nivel}
Código: {codigo}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Descripción:
{descripcion}

Este aviso se ha generado automáticamente.
"""

    enviado = enviar_correo(asunto, mensaje)

    if enviado:
        marcar_correo_alarma_enviado(codigo)

    return True


def resolver_alarma(codigo, titulo_resolucion):
    """
    Resuelve una alarma activa y envía un correo de recuperación.
    """

    alarma = obtener_alarma_activa(codigo)

    if not alarma:
        return False

    resolver_alarma_bd(codigo)
    registrar_evento("ALARMA", "RESUELTA", titulo_resolucion)

    asunto = f"[RESUELTA] {titulo_resolucion}"

    mensaje = f"""
CONTROL DE MANTENIMIENTO DE RIEGO DE SANTA FE

Alarma resuelta.

Código: {codigo}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Detalle:
{titulo_resolucion}
"""

    enviar_correo(asunto, mensaje)

    return True
