import RPi.GPIO as GPIO
import time


available_pins = list(range(0, 30, 1))
available_pins.remove(21)
available_pins.remove(25)
available_pins.remove(9)
available_pins.remove(10)

# available_pins = [5,6,7,8]

# Set the type of GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

try:
    # Server control
    for pin in available_pins:
        # cycle_val = (angle/36) + 7.5
        GPIO.setup(pin, GPIO.OUT)
        servo = GPIO.PWM(pin, 50)  # 50hz
        servo.start(7.5)
        for t in [x / 10 for x in range(50, 100, 20)]:
            print("\nPin: {} t: {}\n".format(pin, t))
            time.sleep(0.5)
            servo.ChangeDutyCycle(t)  # set horizontal servo rotation angle

        servo.stop()

except KeyboardInterrupt:
    GPIO.cleanup()
    servo.stop()

servo.stop()
GPIO.cleanup()
