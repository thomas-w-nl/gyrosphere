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
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)

    def run(self):
        for i in range(0,3):
            # Zet de LED aan.
            GPIO.output(26, self.r)
            GPIO.output(20, self.b)
            GPIO.output(21, self.g)
            sleep(.4)
            # Zet de LED uit.
            GPIO.output(26, 0)
            GPIO.output(20, 0)
            GPIO.output(21, 0)
            sleep(0.4)

    def set_color(self, r, g, b):
        self.r = r
        self.b = b
        self.g = g

if __name__ == "__main__":
    led_light = Led_light(1, 0, 0)
    led_light.setName("Led Light")
    led_light.run()