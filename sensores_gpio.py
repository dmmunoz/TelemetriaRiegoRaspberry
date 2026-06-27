import RPi.GPIO as GPIO

PIN_BOYA = 17        # Pin físico 11
PIN_TRASVASE = 23    # Pin físico 16
PIN_RIEGO = 18       # Pin físico 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Boya: puente GPIO17-GND = nivel bajo
GPIO.setup(PIN_BOYA, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Rain Bird: puente GPIO24-GND = riego activo
GPIO.setup(PIN_RIEGO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Salida trasvase
GPIO.setup(PIN_TRASVASE, GPIO.OUT)
GPIO.output(PIN_TRASVASE, GPIO.LOW)


def leer_nivel_agua():
    if GPIO.input(PIN_BOYA) == GPIO.LOW:
        return "BAJO"
    return "CORRECTO"


def leer_riego():
    if GPIO.input(PIN_RIEGO) == GPIO.LOW:
        return "ACTIVO"
    return "PARADO"


def activar_salida_trasvase():
    GPIO.output(PIN_TRASVASE, GPIO.HIGH)


def parar_salida_trasvase():
    GPIO.output(PIN_TRASVASE, GPIO.LOW)
