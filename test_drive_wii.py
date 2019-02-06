# Python 2

import RPi.GPIO as GPIO
import time
import cwiid


def motor_forward():
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, True)
	GPIO.output(IN2, False)
	GPIO.output(IN3, True)
	GPIO.output(IN4, False)


def motor_backward():
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, False)
	GPIO.output(IN2, True)
	GPIO.output(IN3, False)
	GPIO.output(IN4, True)


def motor_turn_left():
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, True)
	GPIO.output(IN2, False)
	GPIO.output(IN3, False)
	GPIO.output(IN4, True)


def motor_turn_right():
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



print('Press 1+2 on your Wiimote now...')
wm = None
i=2
while not wm:
	try:
		wm = cwiid.Wiimote()
	except RuntimeError:
		if (i>5):
			print("cannot create connection")
			quit()
		print("Error opening wiimote connection")
		print("attempt " + str(i))
		i +=1

wm.led = 1

wm.rpt_mode = cwiid.RPT_ACC | cwiid.RPT_BTN

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



# Motor initialized to LOW
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

wm.led = 1
time.sleep(2)
print("Now in Control")
try:
	delay = 0.03
	while wm.state["buttons"] == 0:
		x, y, z = wm.state["acc"]
		print(x,y,z)
		forward = True
		leftward = True

		roll = 130 - x # mapped to throttle
		if roll > 0:
			forward = False
		roll_on = abs(roll / 25.0)
		if roll_on > 0.999:
			roll_on = 0.999
		roll_off = 1 - roll_on

		pitch = 130 - y # mapped to turns
		if pitch > 0:
			leftward = False
		pitch_on = abs(pitch / 25.0)
		if pitch_on > 0.999:
			pitch_on =  0.999
		pitch_off = 1 - pitch_on

		Motor_Stop()
		time.sleep(delay * roll_off)

		if forward:
			motor_forward()
		else:
			motor_backward()
		time.sleep(delay * roll_on)


except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
