import RPi.GPIO as GPIO
import time

available_pins = [3, 5, 7, 11, 13, 15, 19, 21, 23, 29, 31, 33, 35, 37, 8, 10, 12, 16, 18, 22, 24, 26, 32, 36, 38, 40]

# Set the type of GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

try:
    # Server control
    for pin in available_pins:
        # cycle_val = (angle/36) + 7.5
        print("\nPin: {}\n".format(pin))
        GPIO.setup(pin, GPIO.OUT)  # Horizontal servo port servo7
        servo = GPIO.PWM(pin, 50)  # 50hz
        servo.start(2.5)
        for t in [x / 10 for x in range(25, 125)]:
            print("t is {}".format(t))
            servo.ChangeDutyCycle(t)  # set horizontal servo rotation angle
            time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    servo.stop()

GPIO.cleanup()
servo.stop()
