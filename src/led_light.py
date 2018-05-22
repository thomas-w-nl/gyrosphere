import RPi.GPIO as GPIO
from time import sleep

class led_light:

    def light_on(red, green, blue):
        GPIO.setup(4, GPIO.OUT)
        GPIO.setmode(GPIO.BCM)

        # Zet de LED aan.
        GPIO.output(4, 1)
        sleep(1)

        # Zet de LED uit.
        GPIO.output(4, 0)
        sleep(0.5)

        GPIO.cleanup()
        Color = namedtuple('RGB', red, green, blue)