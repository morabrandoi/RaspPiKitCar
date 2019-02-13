# Python 2

import RPi.GPIO as GPIO
import time
import cwiid
import math

FREQ = 60

# Set the type of GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor drive interface definition
ENABLE_LEFT = 13  # L298 Enable A  # enabled left side?
ENABLE_RIGHT = 20  # L298 Enable B  # enabled right side?
LEFT_FORWARD = 19  # Motor interface 1 # motor forward left
LEFT_REVERSE = 16  # Motor interface 2 # motor reverse left
RIGHT_FORWARD = 21  # Motor interface 3 # motor forward right
RIGHT_REVERSE = 26  # Motor interface 4 # motor reverse right
LIGHTS = [25, 9, 10] # LED lights on shield

# Motor initialized to LOW
GPIO.setup(ENABLE_LEFT, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LEFT_FORWARD, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LEFT_REVERSE, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENABLE_RIGHT, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RIGHT_FORWARD, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RIGHT_REVERSE, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(LIGHTS[0], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LIGHTS[1], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LIGHTS[2], GPIO.OUT, initial=GPIO.HIGH)

LF_PWM = GPIO.PWM(LEFT_FORWARD, FREQ)
LR_PWM = GPIO.PWM(LEFT_REVERSE, FREQ)
RF_PWM = GPIO.PWM(RIGHT_FORWARD, FREQ)
RR_PWM = GPIO.PWM(RIGHT_REVERSE, FREQ)

GPIO.output(ENABLE_LEFT, True)
GPIO.output(ENABLE_RIGHT, True)

LF_PWM.start(0)
LR_PWM.start(0)
RF_PWM.start(0)
RR_PWM.start(0)

for _ in range(3):
    for light_pin_num in LIGHTS:
        GPIO.output(light_pin_num, False)
        time.sleep(0.08)
    for light_pin_num in LIGHTS:
        GPIO.output(light_pin_num, True)
        time.sleep(0.08)

print('Press 1+2 on your Wiimote now...')
wm = None
i = 2
while not wm:
    try:
        wm = cwiid.Wiimote()
    except RuntimeError:
        if (i > 5):
            print("cannot create connection")
            quit()
        print("Error opening wiimote connection")
        print("attempt " + str(i))
        i += 1
del i
time.sleep(0.5)

wm.led = 1
wm.rpt_mode = cwiid.RPT_ACC | cwiid.RPT_BTN

print("Now in Control")


def motor_stop():
    GPIO.output(ENABLE_LEFT, False)
    GPIO.output(ENABLE_RIGHT, False)
    GPIO.output(LEFT_FORWARD, False)
    GPIO.output(LEFT_REVERSE, False)
    GPIO.output(RIGHT_FORWARD, False)
    GPIO.output(RIGHT_REVERSE, False)


# return pitch and roll
def get_remote_data():
    x, y, z = wm.state["acc"]
    # print(x, y, z)

    roll = (130 - x) / 25.0  # mapped to forward
    if roll >= 1.0:
        roll = 0.999
    elif roll <= -1.0:
        roll = -0.999

    pitch = (130 - y) / 25.0  # mapped to left righty
    if pitch >= 1.0:
        pitch = 0.999
    elif pitch <= -1.0:
        pitch = -0.999

    return (pitch, roll)


# returns radius angle
def clip_angles_to_circle(pit, rol):
    x = pit
    y = rol
    radius = math.hypot(x, y)
    if radius >= 1:
        radius = 1
    angle = math.atan2(y, x)
    return (radius, angle)


# takes in pitch and roll, (lateral, longitudinal)
# returns left, right
def map_to_left_right(pit, rol):
    radius, theta = clip_angles_to_circle(pit, rol)

    x = radius * math.cos(theta)
    y = radius * math.sin(theta)

    u = (x * math.cos(-1 * math.pi / 4)) - (y * math.sin(-1 * math.pi / 4))
    v = (y * math.cos(-1 * math.pi / 4)) + (x * math.sin(-1 * math.pi / 4))

    u2 = u * u
    v2 = v * v
    twosqrt2 = 2.0 * math.sqrt(2.0)
    subtermx = 2.0 + u2 - v2
    subtermy = 2.0 - u2 + v2
    termx1 = subtermx + u * twosqrt2
    termx2 = subtermx - u * twosqrt2
    termy1 = subtermy + v * twosqrt2
    termy2 = subtermy - v * twosqrt2

    epsilon = 0.0001
    if abs(termx2) < epsilon:
        termx2 = 0.0
    if abs(termy2) < epsilon:
        termy2 = 0.0
    if abs(termx1) < epsilon:
        termx1 = 0.0
    if abs(termy1) < epsilon:
        termy1 = 0.0

    left_motor_speed = 0.5 * math.sqrt(termx1) - 0.5 * math.sqrt(termx2)
    right_motor_speed = 0.5 * math.sqrt(termy1) - 0.5 * math.sqrt(termy2)
    # both speeds are in range (-1,1) at this point

    return (left_motor_speed, right_motor_speed)


def write_to_motors(left, right):
    abs_left_speed = max(0, min(abs(left) * 100, 100))
    abs_right_speed = max(0, min(abs(right) * 100, 100))
    l_forwards = left > 0
    r_forwards = right > 0
    [LR_PWM.ChangeDutyCycle, LF_PWM.ChangeDutyCycle][not l_forwards](0)
    [LR_PWM.ChangeDutyCycle, LF_PWM.ChangeDutyCycle][l_forwards](abs_left_speed)
    [RR_PWM.ChangeDutyCycle, RF_PWM.ChangeDutyCycle][not r_forwards](0)
    [RR_PWM.ChangeDutyCycle, RF_PWM.ChangeDutyCycle][r_forwards](abs_right_speed)



def output_loop():
    while wm.state["buttons"] != 15:
        pitch, roll = get_remote_data()
        left, right = map_to_left_right(pitch, roll)
        write_to_motors(left, right)



if __name__ == "__main__":
    try:
        output_loop()
    except KeyboardInterrupt:
        GPIO.cleanup()

    GPIO.cleanup()
