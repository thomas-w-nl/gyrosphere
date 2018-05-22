from time import sleep
import cv2
from target_detection import get_target
from motor import Motor


class GyrosphereAutopilot:
    def __init__(self, event):
        self.bt_event = event

        self.cap = cv2.VideoCapture(-1)
        sleep(.2)

        self.motor_r = Motor(6, 5, 13)
        self.motor_l = Motor(16, 18, 12)

    def pilot(self):

        while True:
            # the event is set if there is no bt connection
            self.bt_event.wait()

            spd = 100
            target_direction = get_target(self.cap)
            print("target direction:", target_direction)

            if target_direction <= 0.2:
                # turn left
                self.motor_l.drive("r", spd)
                self.motor_r.drive("f", spd)
                self.led_light.light_on(255, 0, 0)

            elif target_direction >= 0.8:
                # turn right
                self.motor_l.drive("f", spd)
                self.motor_r.drive("r", spd)
                self.led_light.light_on(0, 255, 0)

            elif target_direction == -1:
                # turn to find something
                self.motor_l.drive("r", spd)
                self.motor_r.drive("f", spd)

            elif 0.6 > target_direction > 0.4:
                self.motor_l.drive("f", spd)
                self.motor_r.drive("f", spd)
                self.led_light.light_on(0, 0, 255)

            elif 0.8 > target_direction >= 0.6:
                spd = 50
                self.motor_l.drive("f", spd)
                self.motor_r.drive("r", spd)

            elif 0.4 >= target_direction > 0.2:
                spd = 50
                self.motor_l.drive("r", spd)
                self.motor_r.drive("f", spd)



        # go to target

        # if no target is found go look for one

        # if battery is empty shutdown
