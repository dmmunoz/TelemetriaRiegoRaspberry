from datetime import datetime, timedelta
import sqlite3

from emailer import enviar_correo

DB_PATH = "/home/santafe/telemetria/database/telemetria.db"


def obtener_eventos_semana():
    desde = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT fecha, tipo, estado, detalle
        FROM eventos
        WHERE fecha >= ?
        ORDER BY fecha DESC
        """,
        (desde,)
    )

    eventos = cursor.fetchall()
    conn.close()
    return eventos


def generar_informe():
    eventos = obtener_eventos_semana()

    total_riegos = sum(1 for e in eventos if e[1] == "RIEGO" and "INICIADO" in e[2])
    total_trasvases = sum(1 for e in eventos if e[1] == "TRASVASE" and "INICIADO" in e[2])
    alarmas = [e for e in eventos if e[1] in ("SEGURIDAD", "ALARMA", "SISTEMA") and e[2] in ("BLOQUEADO", "ALARMA")]

    texto = []
    texto.append("INFORME SEMANAL - CONTROL DE RIEGO SANTA FE")
    texto.append("")
    texto.append(f"Fecha del informe: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    texto.append("")
    texto.append("RESUMEN")
    texto.append(f"- Riegos detectados esta semana: {total_riegos}")
    texto.append(f"- Trasvases iniciados esta semana: {total_trasvases}")
    texto.append(f"- Alarmas registradas: {len(alarmas)}")
    texto.append("")

    texto.append("ÚLTIMOS EVENTOS")
    if eventos:
        for fecha, tipo, estado, detalle in eventos[:20]:
            texto.append(f"- {fecha} | {tipo} | {estado} | {detalle}")
    else:
        texto.append("- No hay eventos registrados esta semana.")

    texto.append("")
    texto.append("Sistema automático de mantenimiento de riego.")
    texto.append("Comunidad Santa Fe.")

    return "\n".join(texto)


if __name__ == "__main__":
    asunto = "Informe semanal - Control de Riego Santa Fe"
    mensaje = generar_informe()
    enviar_correo(asunto, mensaje)
