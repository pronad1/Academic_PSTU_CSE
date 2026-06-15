import RPi.GPIO as GPIO
import time

TRIG = 24
ECHO = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():

    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start

    distance = duration * 17150

    return round(distance, 2)

try:

    while True:

        d = get_distance()

        print("Distance:", d, "cm")

        time.sleep(1)

except KeyboardInterrupt:

    GPIO.cleanup()
