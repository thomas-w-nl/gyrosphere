import RPi.GPIO as GPIO
from time import sleep
import threading
from threading import Thread

GPIO.setmode(GPIO.BCM)

class Led_light(Thread):
    def __init__(self, r, g, b):
        Thread.__init__(self)
        self.r = r
        self.b = b
        self.g = g

    def run(self):

        GPIO.setup(4, GPIO.OUT)
        # Zet de LED aan.
        GPIO.output(4, 1)
        sleep(.5)
        # Zet de LED uit.
        GPIO.output(4, 0)
        sleep(0.5)

    def set_color(self, r, g, b):
        self.r = r
        self.b = b
        self.g = g

