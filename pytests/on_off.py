"""
on_off.py: Basic test for toggling a DIO pin high
"""

import time
from labjack import ljm

dio = "FIO2"

def actuate(on):
	global dio
	state = int(on)
	ljm.eWriteName(handle, dio, state)

if __name__ == "__main__":
	handle = ljm.openS("T7", "ANY", "ANY")

	actuate(True)
	time.sleep(3)
	actuate(False)

	ljm.close(handle)
