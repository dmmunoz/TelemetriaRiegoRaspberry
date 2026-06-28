import RPi.GPIO as GPIO
from config import PIN_BOYA, PIN_TRASVASE, PIN_RIEGO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIN_BOYA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_RIEGO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
