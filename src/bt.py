# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
from motor import Motor

motor_r = Motor(6, 5, 13)
motor_l = Motor(16, 18, 12)

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_sock, "SampleServer",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  #                   protocols = [ OBEX_UUID ]
                  )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        #print("received [%s]" % data)
        ctl = chr(data[0])
        print(ctl)

        if ctl == "1":
            spd = 100  # int(input("speed(0-100):"))
            motor_l.drive("f", spd)
            motor_r.drive("f", spd)

        if ctl == "2":
            spd = 100  # int(input("speed(0-100):"))
            motor_l.drive("r", spd)
            motor_r.drive("r", spd)

        if ctl == "9":
            spd = 100  # input("force(0-100):")
            motor_l.brake(spd)
            motor_r.brake(spd)

        if ctl == "3":
            spd = 100  # int(input("speed(0-100):"))
            motor_l.drive("r", spd)
            motor_r.drive("f", spd)

        if ctl == "4":
            spd = 100  # int(input("speed(0-100):"))
            motor_l.drive("f", spd)
            motor_r.drive("r", spd)

        if ctl == "q":
            break


except IOError:
    pass

motor_l.drive("f", 0)
motor_r.drive("f", 0)

print("disconnected")

client_sock.close()
server_sock.close()

print("all done")
