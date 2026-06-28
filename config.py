# =========================
# CONFIGURACIÓN GENERAL
# =========================

NOMBRE_SISTEMA = "SantaFe Water Control"
NOMBRE_COMUNIDAD = "Comunidad Santa Fe"

# =========================
# GPIO - Raspberry Pi
# =========================

PIN_BOYA = 17        # Pin físico 11
PIN_TRASVASE = 23    # Pin físico 16
PIN_RIEGO = 18       # Pin físico 12

# =========================
# TIEMPOS DE SEGURIDAD
# =========================

TIEMPO_CONFIRMACION_BAJO = 5          # segundos
TIEMPO_MAX_TRASVASE = 6 * 60 * 60     # 6 horas
TIEMPO_MAX_RIEGO = 90 * 60            # 90 minutos

# =========================
# ALARMAS
# =========================

DIAS_MAX_SIN_RIEGO = 7
HORAS_MAX_ALJIBE_BAJO = 48

# =========================
# BASE DE DATOS
# =========================

DB_PATH = "/home/santafe/telemetria/database/telemetria.db"
