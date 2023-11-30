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

    run = threading.Thread(target= controller.run) #, 'val' : v}) #, args=(v))
    read = threading.Thread(target=controller.read, daemon= True) #, 'val' : v}) #, args=(v))

    run.start()
    read.start()

    
    run.join()
    read.join()

    # TODO: make data file available to close here

    #reads = threading.Thread(target=sensors_read, kwargs={'handle' : handle})
    #updates = threading.Thread(target=controller.run)

    # updates.run()
    # updates.join()

    if use_labjack:
        ljm.close(handle)