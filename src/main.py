"""
main.py: The entry point for the hybrid control program
"""

from labjack import ljm
import sys

from controller import Controller

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--no-labjack":
        labjack = False
        handle = None
    else:
        labjack = True
        handle = ljm.openS("T7", "ANY", "ANY")

    ljm.eWriteName(handle, "FIO0", 0)
    ljm.eWriteName(handle, "FIO1", 0)

    hold = input("Press any key to continue: ")

    controller = Controller(handle)
    controller.run()

    if labjack:
        ljm.close(handle)