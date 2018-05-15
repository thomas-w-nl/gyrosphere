from src.battery import Battery
from src.target_detection import get_target
from src.motor import Motor

battery = Battery()

motor_r = Motor(6, 5, 13)
motor_l = Motor(16, 18, 12)

target_direction = get_target()

spd = 100

no_bt = True

while no_bt:

    if target_direction <= 0.3:
        # turn left
        motor_l.drive("r", spd)
        motor_r.drive("f", spd)

    elif target_direction >= 0.7:
        # turn right
        motor_l.drive("f", spd)
        motor_r.drive("r", spd)

    elif target_direction == -1:
        # turn right
        motor_l.drive("r", spd)
        motor_r.drive("f", spd)

    elif 0.7 > target_direction > 0.3:
        motor_l.drive("f", spd)
        motor_r.drive("f", spd)






# go to target

# if no target is found go look for one

# if battery is empty shutdown