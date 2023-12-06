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

    controller = Controller(handle)

    run = threading.Thread(target= controller.run)
    read = threading.Thread(target=controller.read, daemon= True)

    run.start()
    read.start()

    
    run.join()
    read.join()

    # make data file available to close here ?

    if use_labjack:
        ljm.close(handle)