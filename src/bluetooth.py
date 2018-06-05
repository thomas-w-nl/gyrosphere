from bluetooth import *
from motor import Motor
from led_light import Led_light
from threading import Thread


class BluetoothThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.bt_event = event
        # instellen van de motoren op de fysieke pins
        self.motor_r = Motor(6, 5, 13)
        self.motor_l = Motor(16, 18, 12)

        # Standaard bluetooth settings
        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", PORT_ANY))
        self.server_sock.listen(1)

        # port die het zelfde is op de app
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        # aanbieden van de socket
        advertise_service(self.server_sock, "Gyrosphere_control_server",
                          service_id=self.uuid,
                          service_classes=[self.uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          )

    def run(self):

        # accept connections forever
        while True:
            print("Waiting for bluetooth connection")

            # blocking, dus we wachten tot een nieuwe verbinding ontstaat
            client_sock, client_info = self.server_sock.accept()

            # block main autopilot thread
            self.bt_event.clear()

            print("Accepted connection from ", client_info)

            # blink blue light
            led_light = Led_light(0, 0, 1)

            led_light.run()

            try:
                # keep accepting commands from connection until connection is broken
                while True:
                    data = client_sock.recv(1024)

                    if len(data) == 0: break
                    if len(data) > 1000: break
                    # print("received [%s]" % data)

                    # alleen de eerste byte als commandos aan elkaar geplakt zitten
                    ctl1 = chr(data[0])

                    ctl = ""
                    for i in data:
                        ctl += chr(i)

                    print(ctl)

                    spd = 100

                    if ctl1 == "1":
                        self.motor_l.drive("f", spd)
                        self.motor_r.drive("f", spd)
                        led_light = Led_light(0, 0, 1)
                        led_light.run()

                    if ctl1 == "2":
                        self.motor_l.drive("r", spd)
                        self.motor_r.drive("r", spd)

                    if ctl1 == "9":
                        self.motor_l.brake(spd)
                        self.motor_r.brake(spd)

                    if ctl1 == "3":
                        self.motor_l.drive("r", spd)
                        self.motor_r.drive("f", spd)

                    if ctl1 == "4":
                        self.motor_l.drive("f", spd)
                        self.motor_r.drive("r", spd)

                    if ctl == "red":
                        led_light = Led_light(1, 0, 0)
                        led_light.run()

                    if ctl == "yellow":
                        led_light = Led_light(0, 1, 1)
                        led_light.run()

                    if ctl == "green":
                        led_light = Led_light(0, 1, 0)
                        led_light.run()

                    if ctl == "q":
                        break



            except IOError:
                pass
            print("disconnected")

            client_sock.close()

            # unblock thread
            self.bt_event.set()
