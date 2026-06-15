from gpiozero import AngularServo
from time import sleep

servo = AngularServo(
    26,
    min_angle=0,
    max_angle=180
)

while True:

    print("LEFT")
    servo.angle = 0
    sleep(2)

    print("CENTER")
    servo.angle = 90
    sleep(2)

    print("RIGHT")
    servo.angle = 180
    sleep(2)
