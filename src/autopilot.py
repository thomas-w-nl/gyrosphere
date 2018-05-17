from time import sleep
import cv2
from target_detection import get_target
from motor import Motor

cap = cv2.VideoCapture(-1)
sleep(.2)

motor_r = Motor(6, 5, 13)
motor_l = Motor(16, 18, 12)

print("Started! getting target")
target_direction = get_target(cap)

spd = 50


no_bt = True

while no_bt:

    target_direction = get_target(cap)
    print("target direction:",target_direction)

    if -0.1 < target_direction <= 0.3:
        # turn right
        motor_l.drive("f", spd)
        motor_r.drive("r", spd)

    elif target_direction >= 0.7:
        # turn left
        motor_l.drive("r", spd)
        motor_r.drive("f", spd)

    elif target_direction == -1:
        # # turn to find something
        # motor_l.drive("r", spd)
        # motor_r.drive("f", spd)
        motor_l.brake(spd)
        motor_r.brake(spd)

    elif 0.7 > target_direction > 0.3:
        motor_l.drive("f", spd)
        motor_r.drive("f", spd)





# go to target

# if no target is found go look for one

# if battery is empty shutdown