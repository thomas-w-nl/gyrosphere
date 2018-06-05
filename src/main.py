from queue import Queue
from time import sleep

import threading
from threading import Thread

from autopilot import GyrosphereAutopilot
from bluetooth import BluetoothThread


if __name__ == "__main__":

    print("Starting GyroSphere v1")



    # set the event so autopilot can start
    bt_event = threading.Event()
    bt_event.set()

    # Start the thread to accept incomming connections
    bt_thread = BluetoothThread(bt_event)
    bt_thread.start()

    # start the autopilot
    gap = GyrosphereAutopilot(bt_event)
    gap.pilot()

    # wait for the autopilot thread to get stopped
    gap.join()



