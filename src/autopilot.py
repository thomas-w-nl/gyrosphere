from src.battery import Battery
from src.motion_detection import get_target
from src.motor import Motor

battery = Battery()

motor_r = Motor(6, 5, 13)
motor_l = Motor(16, 18, 12)

target_direction = get_target()

# go to target

# if no target is found go look for one

# if battery is empty shutdown