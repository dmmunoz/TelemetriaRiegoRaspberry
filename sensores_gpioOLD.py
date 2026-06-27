import RPi.GPIO as GPIO

PIN_BOYA = 17       # Pin físico 11
PIN_TRASVASE = 23   # Pin físico 16

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIN_BOYA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_TRASVASE, GPIO.OUT)

GPIO.output(PIN_TRASVASE, GPIO.LOW)


def leer_nivel_agua():
    """
    Sin puente / boya abierta = CORRECTO
    Puente GPIO17-GND / boya cerrada = BAJO
    """
    if GPIO.input(PIN_BOYA) == GPIO.LOW:
        return "BAJO"
    return "CORRECTO"


def activar_salida_trasvase():
    GPIO.output(PIN_TRASVASE, GPIO.HIGH)


def parar_salida_trasvase():
    GPIO.output(PIN_TRASVASE, GPIO.LOW)
