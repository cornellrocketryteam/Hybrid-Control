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

    if use_labjack:
        run = threading.Thread(target= controller.run)
        read = threading.Thread(target=controller.read, daemon= True)

        run.start()
        read.start()

        
        run.join()
        read.join()
    else:
        controller.run()


    if use_labjack:
        try:
            pass
        finally:
            #log quit
            ljm.close(handle)
