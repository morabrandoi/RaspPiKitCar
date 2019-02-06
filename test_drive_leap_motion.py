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
def set_servo_angle(servo, angle):
	if not (-90.0 <= angle <= 90.0):
		raise Exception("Value of angle out of range")
	cycle_val = (angle/36) + 7.5
	servo.ChangeDutyCycle(cycle_val)


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
HORISERV = 21  # Horizontal servo BCM Pin 21

GPIO.setup(HORISERV, GPIO.OUT)  # Horizontal servo port servo7
horizontal_servo = GPIO.PWM(HORISERV, 50)  # 50HZ
horizontal_servo.start(7.5)


# Motor initialized to LOW
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)


try:
    set_servo_angle(horizontal_servo, -90)
	time.sleep(2)
	Motor_Forward()
	set_servo_angle(0)
	Motor_Backward()
	set_servo_angle(90)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
