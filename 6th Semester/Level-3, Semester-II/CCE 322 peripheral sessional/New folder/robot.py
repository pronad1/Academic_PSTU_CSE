import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)


# Driver 1 Left
M1_IN1 = 17
M1_IN2 = 27
M2_IN1 = 22
M2_IN2 = 23

ENA1 = 18
ENB1 = 12


# Driver 2 Right
M3_IN1 = 5
M3_IN2 = 6
M4_IN1 = 13
M4_IN2 = 19

ENA2 = 16
ENB2 = 20



pins=[
M1_IN1,M1_IN2,
M2_IN1,M2_IN2,
M3_IN1,M3_IN2,
M4_IN1,M4_IN2,
ENA1,ENB1,
ENA2,ENB2
]


for p in pins:
    GPIO.setup(p,GPIO.OUT)



# PWM Speed
pwm1=GPIO.PWM(ENA1,1000)
pwm2=GPIO.PWM(ENB1,1000)

pwm3=GPIO.PWM(ENA2,1000)
pwm4=GPIO.PWM(ENB2,1000)


pwm1.start(80)
pwm2.start(80)
pwm3.start(80)
pwm4.start(80)



def stop():

    for p in [
    M1_IN1,M1_IN2,
    M2_IN1,M2_IN2,
    M3_IN1,M3_IN2,
    M4_IN1,M4_IN2]:

        GPIO.output(p,0)



def forward():

    print("FORWARD")

    # left side
    GPIO.output(M1_IN1,1)
    GPIO.output(M1_IN2,0)

    GPIO.output(M2_IN1,1)
    GPIO.output(M2_IN2,0)


    # right side
    GPIO.output(M3_IN1,1)
    GPIO.output(M3_IN2,0)

    GPIO.output(M4_IN1,1)
    GPIO.output(M4_IN2,0)




def backward():

    print("BACKWARD")

    GPIO.output(M1_IN1,0)
    GPIO.output(M1_IN2,1)

    GPIO.output(M2_IN1,0)
    GPIO.output(M2_IN2,1)


    GPIO.output(M3_IN1,0)
    GPIO.output(M3_IN2,1)

    GPIO.output(M4_IN1,0)
    GPIO.output(M4_IN2,1)





def left():

    print("LEFT")

    # Left reverse

    GPIO.output(M1_IN1,0)
    GPIO.output(M1_IN2,1)

    GPIO.output(M2_IN1,0)
    GPIO.output(M2_IN2,1)


    # Right forward

    GPIO.output(M3_IN1,1)
    GPIO.output(M3_IN2,0)

    GPIO.output(M4_IN1,1)
    GPIO.output(M4_IN2,0)






def right():

    print("RIGHT")


    # Left forward

    GPIO.output(M1_IN1,1)
    GPIO.output(M1_IN2,0)

    GPIO.output(M2_IN1,1)
    GPIO.output(M2_IN2,0)



    # Right reverse

    GPIO.output(M3_IN1,0)
    GPIO.output(M3_IN2,1)

    GPIO.output(M4_IN1,0)
    GPIO.output(M4_IN2,1)





try:

    while True:

        cmd=input(
        "w=forward s=back a=left d=right x=stop : "
        )


        if cmd=="w":
            forward()

        elif cmd=="s":
            backward()

        elif cmd=="a":
            left()

        elif cmd=="d":
            right()

        elif cmd=="x":
            stop()



except KeyboardInterrupt:
    pass


finally:
    stop()
    GPIO.cleanup()
