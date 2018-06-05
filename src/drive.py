from motor import Motor


motor_r = Motor(6, 5, 13)
motor_l = Motor(16, 18, 12)

ctl = "start"

while ctl != "q":
    ctl = input('Choose action (f,b,r,tl,tr,s): ')

    if ctl == "f" or ctl == "r":
        spd = 100 # int(input("speed(0-100):"))
        motor_l.drive(ctl, spd)
        motor_r.drive(ctl, spd)

    if ctl == "b":
        spd = 100 # input("force(0-100):")
        motor_l.brake(spd)
        motor_r.brake(spd)

    if ctl == "tl":
        spd = 100# int(input("speed(0-100):"))
        motor_l.drive("r", spd)
        motor_r.drive("f", spd)

    if ctl == "tr":
        spd = 100 #int(input("speed(0-100):"))
        motor_l.drive("f", spd)
        motor_r.drive("r", spd)

    if ctl == "q":
        motor_l.brake(100)
        motor_r.brake(100)
        break





