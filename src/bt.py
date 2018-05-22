# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
from motor import Motor


class GyroSphereBluetooth:
    def __init__(self, event):
        self.bt_event = event

        self.motor_r = Motor(6, 5, 13)
        self.motor_l = Motor(16, 18, 12)

        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", PORT_ANY))
        self.server_sock.listen(1)

        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service(self.server_sock, "Gyrosphere_control_server",
                          service_id=self.uuid,
                          service_classes=[self.uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          #                   protocols = [ OBEX_UUID ]
                          )

    def handle_bluetooth_connection(self):

        print("Waiting for bluetooth connection")

        client_sock, client_info = self.server_sock.accept()  # blocking
        # block thread
        self.bt_event.clear()

        print("Accepted connection from ", client_info)

        try:
            while True:
                data = client_sock.recv(1024)

                if len(data) == 0: break
                if len(data) > 1000: break
                # print("received [%s]" % data)

                ctl = ""

                for i in data:
                    ctl += chr(i)

                print(ctl)

                if ctl == "1":
                    spd = 100  # int(input("speed(0-100):"))
                    self.motor_l.drive("f", spd)
                    self.motor_r.drive("f", spd)

                if ctl == "2":
                    spd = 100  # int(input("speed(0-100):"))
                    self.motor_l.drive("r", spd)
                    self.motor_r.drive("r", spd)

                if ctl == "9":
                    spd = 100  # input("force(0-100):")
                    self.motor_l.brake(spd)
                    self.motor_r.brake(spd)

                if ctl == "3":
                    spd = 100  # int(input("speed(0-100):"))
                    self.motor_l.drive("r", spd)
                    self.motor_r.drive("f", spd)

                if ctl == "4":
                    spd = 100  # int(input("speed(0-100):"))
                    self.motor_l.drive("f", spd)
                    self.motor_r.drive("r", spd)

                if ctl == "b":
                    pass
                    # switch naar detectie blauw.

                if ctl == "q":
                    break

                client_sock.send("Hello from pi")


        except IOError:
            pass
        print("disconnected")

        client_sock.close()
        # self.server_sock.close()

        # unblock thread
        self.bt_event.set()
