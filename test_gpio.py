import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Leyendo GPIO24...")

while True:
    print(GPIO.input(24))
    time.sleep(0.5)
