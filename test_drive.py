import RPi.GPIO as GPIO
import time


def Motor_Forward():
	print('motor forward')
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, True)
	GPIO.output(IN2, False)
	GPIO.output(IN3, True)
	GPIO.output(IN4, False)


def Motor_Backward():
	print('motor_backward')
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, False)
	GPIO.output(IN2, True)
	GPIO.output(IN3, False)
	GPIO.output(IN4, True)


def Motor_TurnLeft():
	print('motor_turnleft')
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, True)
	GPIO.output(IN2, False)
	GPIO.output(IN3, False)
	GPIO.output(IN4, True)


def Motor_TurnRight():
	print('motor_turnright')
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, False)
	GPIO.output(IN2, True)
	GPIO.output(IN3, True)
	GPIO.output(IN4, False)


def Motor_Stop():
	print('motor_stop')
	GPIO.output(ENA, False)
	GPIO.output(ENB, False)
	GPIO.output(IN1, False)
	GPIO.output(IN2, False)
	GPIO.output(IN3, False)
	GPIO.output(IN4, False)


# Servo angle drive function # angle in degrees [-90, 90] @ 50hz
def SetServo7Angle(angle):
    cycle_val = (angle/36) + 7.5
    Servo7.ChangeDutyCycle(cycle_val)  # set horizontal servo rotation angle
    time.sleep(0.01)


def SetServo8Angle(angle):
    cycle_val = (angle/36) + 7.5
    Servo8.ChangeDutyCycle(cycle_val)  # Set vertical servo rotation angle
    time.sleep(0.01)


# Set the type of GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor drive interface definition
ENA = 13  # //L298 Enable A
ENB = 20  # //L298 Enable B
IN1 = 19  # //Motor interface 1 # motor forward left
IN2 = 16  # //Motor interface 2 # motor reverse left
IN3 = 21  # //Motor interface 3 # motor forward right
IN4 = 26  # //Motor interface 4 # motor reverse right

# Server control
SER7 = 6  # Vertical servo  port servo7
SER8 = 12  # Horizontal servo port servo8

GPIO.setup(SER7, GPIO.OUT)  # Horizontal servo port servo7
GPIO.setup(SER8, GPIO.OUT)  # Vertical servo port servo8
Servo7 = GPIO.PWM(SER7, 50)  # 50HZ
Servo7.start(7.5)
Servo8 = GPIO.PWM(SER8, 50)  # 50Hz
Servo8.start(7.5)

# Motor initialized to LOW
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)


try:
    for t in range(-90, 91, 1):
        time.sleep(0.02)
        print("t: {}".format(t))
        SetServo7Angle(t)
        SetServo8Angle(t)
except KeyboardInterrupt:
    GPIO.cleanup()
    Servo7.stop()
    Servo8.stop()

GPIO.cleanup()
Servo7.stop()
Servo8.stop()
