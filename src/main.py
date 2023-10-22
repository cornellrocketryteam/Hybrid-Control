"""
main.py: The entry point for the hybrid control program
"""

import threading
from labjack import ljm
import sys

from util import use_labjack

from controller import Controller

if __name__ == "__main__":
    if use_labjack:
        handle = ljm.openS("T7", "ANY", "ANY")
    else:
        handle = None

    #ljm.eWriteName(handle, "FIO0", 0)
    #ljm.eWriteName(handle, "FIO1", 0)

    #hold = input("Press any key to continue: ")

    controller = Controller(handle)
    controller.run()

    #reads = threading.Thread(target=sensors_read, kwargs={'handle' : handle})
    #updates = threading.Thread(target=controller.run)

    # updates.run()
    # updates.join()

    if use_labjack:
        ljm.close(handle)