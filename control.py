import time
from datetime import datetime

from database import obtener_estado, actualizar_estado, registrar_evento
from sensores_gpio import (
    leer_nivel_agua,
    leer_riego,
    activar_salida_trasvase,
    parar_salida_trasvase
)

TIEMPO_CONFIRMACION_BAJO = 5
TIEMPO_MAX_TRASVASE = 6 * 60 * 60

inicio_trasvase = None


def ciclo_control():
    global inicio_trasvase

    estado = obtener_estado()

    nivel = leer_nivel_agua()
    riego = leer_riego()

    bloqueo = estado["bloqueo"]["valor"]
    trasvase = estado["trasvase"]["valor"]
    riego_anterior = estado["riego"]["valor"]

    actualizar_estado("nivel_agua", nivel)

    # Registro Rain Bird
    if riego != riego_anterior:
        actualizar_estado("riego", riego)

        if riego == "ACTIVO":
            registrar_evento("RIEGO", "INICIADO", "Señal detectada desde borne M Rain Bird")
        else:
            registrar_evento("RIEGO", "FINALIZADO", "Señal Rain Bird apagada")

    # Seguridad
    if bloqueo == "SI":
        parar_salida_trasvase()
        actualizar_estado("trasvase", "PARADO")
        return

    # Nivel bajo: iniciar trasvase tras confirmación
    if nivel == "BAJO" and trasvase != "ACTIVO":
        time.sleep(TIEMPO_CONFIRMACION_BAJO)

        if leer_nivel_agua() == "BAJO":
            activar_salida_trasvase()
            actualizar_estado("trasvase", "ACTIVO")
            inicio_trasvase = datetime.now()
            registrar_evento("TRASVASE", "INICIADO", "Nivel bajo confirmado")
        return

    # Nivel correcto: parar trasvase
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

    # Bloqueo por tiempo máximo
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
