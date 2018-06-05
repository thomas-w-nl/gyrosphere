from queue import Queue
from time import sleep

import threading
from threading import Thread

from autopilot import GyrosphereAutopilot
from bt import GyroSphereBluetooth


class BluetoothThread(Thread):

    def __init__(self, event):
        Thread.__init__(self)
        self.bt_event = event

    def run(self):

        gbt = GyroSphereBluetooth(bt_event)
        # bt loop
        while True:
            gbt.handle_bluetooth_connection()





if __name__ == "__main__":

    print("Starting")




    bt_event = threading.Event()

    #set it so autopilot can startz
    bt_event.set()

    tr = BluetoothThread(bt_event)
    gap = GyrosphereAutopilot(bt_event)
    tr.setName("Bluetooth")
    tr.start()

    # autopilot loop
    while True:

        # the event is set if there is no bt connection

        gap.pilot()

        # run autopilot



