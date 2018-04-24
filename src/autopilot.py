from src.battery import Battery
from src.motion_detection import get_target
from src.motor import Motor

battery = Battery()

motor_r = Motor(6, 5, 13)
motor_l = Motor(16, 18, 12)

target_direction = get_target()


def rotate():
    spd = 100

    if target_direction == 0:
        motor_l.drive("r", spd)
        motor_r.drive("f", spd)

    elif target_direction == 1:
        motor_l.drive("f", spd)
        motor_r.drive("r", spd)

    elif target_direction == 0.5:
        motor_l.drive("f", spd)
        motor_r.drive("f", spd)

    elif target_direction == -1:
        motor_l.drive("f", spd)
        motor_r.drive("r", spd)


def shut_down():
    spd = 0

    if battery.get_spanning() == 3.70:
        motor_l.brake(spd)
        motor_r.brake(spd)

# go to target

# if no target is found go look for one

# if battery is empty shutdown

# 3.6-4.2 voor battery
