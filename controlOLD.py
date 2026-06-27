import time
from datetime import datetime, timedelta

from database import obtener_estado, actualizar_estado, registrar_evento
from sensores_gpio import leer_nivel_agua, activar_salida_trasvase, parar_salida_trasvase

TIEMPO_CONFIRMACION_BAJO = 5          # segundos
TIEMPO_MAX_TRASVASE = 6 * 60 * 60     # 6 horas

inicio_trasvase = None


def segundos_desde(fecha_txt):
    try:
        fecha = datetime.strptime(fecha_txt, "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - fecha).total_seconds()
    except Exception:
        return 0


def ciclo_control():
    global inicio_trasvase

    estado = obtener_estado()
    nivel = leer_nivel_agua()
    bloqueo = estado["bloqueo"]["valor"]
    trasvase = estado["trasvase"]["valor"]

    actualizar_estado("nivel_agua", nivel)

    if bloqueo == "SI":
        parar_salida_trasvase()
        actualizar_estado("trasvase", "PARADO")
        return

    if nivel == "BAJO" and trasvase != "ACTIVO":
        time.sleep(TIEMPO_CONFIRMACION_BAJO)

        if leer_nivel_agua() == "BAJO":
            activar_salida_trasvase()
            actualizar_estado("trasvase", "ACTIVO")
            inicio_trasvase = datetime.now()
            registrar_evento("TRASVASE", "INICIADO", "Nivel bajo confirmado")
        return

    if nivel == "CORRECTO" and trasvase == "ACTIVO":
        parar_salida_trasvase()
        actualizar_estado("trasvase", "PARADO")

        if inicio_trasvase:
            duracion = datetime.now() - inicio_trasvase
            detalle = f"Trasvase completado. Duración: {str(duracion).split('.')[0]}"
        else:
            detalle = "Trasvase completado"

        registrar_evento("TRASVASE", "FINALIZADO", detalle)
        inicio_trasvase = None
        return

    if trasvase == "ACTIVO":
        if inicio_trasvase is None:
            inicio_trasvase = datetime.now()

        if (datetime.now() - inicio_trasvase).total_seconds() > TIEMPO_MAX_TRASVASE:
            parar_salida_trasvase()
            actualizar_estado("trasvase", "PARADO")
            actualizar_estado("bloqueo", "SI")
            registrar_evento(
                "SEGURIDAD",
                "BLOQUEADO",
                "Tiempo máximo de trasvase superado: 6 horas"
            )
