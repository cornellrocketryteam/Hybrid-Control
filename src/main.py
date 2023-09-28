"""
main.py: The entry point for the hybrid control program
"""

from labjack import ljm
import time


from test_stand import TestStand
from controller import Controller

if __name__ == "__main__":
    #handle = ljm.openS("T7", "ANY", "ANY")
    handle = None

    controller = Controller(handle)
    controller.run()

    #ljm.close(handle)