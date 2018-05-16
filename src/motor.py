import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
class Motor:

    def __init__(self, pin1, pin2, pin_enable):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
        GPIO.setup(pin_enable, GPIO.OUT)

        self._pin1 = pin1
        self._pin2 = pin2
        self._pin_enable_pwm = GPIO.PWM(pin_enable, 100)
        self._pin_enable_pwm.start(0)

    def __del__(self):
        self.brake(100)
        GPIO.cleanup()

    def drive(self, direction, speed):
        # direction
        """
        Start the motor in the indicated direction and speed.
        :param direction: The direction which the should motor turn ["f","r"]
        :param speed: The speed at which the motor should turn [0-100]
        """
        if direction == "f":

            GPIO.output(self._pin1, GPIO.HIGH)
            GPIO.output(self._pin2, GPIO.LOW)

        elif direction == "r":
            GPIO.output(self._pin1, GPIO.LOW)
            GPIO.output(self._pin2, GPIO.HIGH)
        else:
            raise Exception("Unknown motor direction")

        # speed
        if 0 <= speed <= 100:
            self._pin_enable_pwm.ChangeDutyCycle(speed)
        else:
            raise Exception("Motor speed out of range")

    def brake(self, pwr):
        """
        A special braking configuration to allow control over the braking force.
        :param pwr: The braking force, where zero is freewheeling. [0-100]
        """
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.LOW)
        self._pin_enable_pwm.ChangeDutyCycle(int(pwr))
