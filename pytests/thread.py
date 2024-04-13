"""
threads.py: A simple test to write to and read from a labjack simultaneously.
"""

from labjack import ljm
import threading
import time


def read_fn(handle):
	print("tryig to read: ", handle)
	names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US"]
	aValues = [199, 10.0, 0, 0]
	numFrames = len(names)
	ljm.eWriteNames(handle, numFrames, names, aValues)

	# Setup and call eReadName to read AIN0 from the LabJack.
	name = "AIN0"
	while True:
		print("reading")
		result = ljm.eReadName(handle, name)
		print("after read")


def write_fn(handle):
	print("tryign to write: ", handle)
	state = True
	while True:
		print("writng")
		result = ljm.eWriteName(handle, "FIO2", int(state))
		state = not state
		time.sleep(1)
		print("after write")


if __name__ == "__main__":
	handle = ljm.openS("T7", "ANY", "ANY")
	print("found handle: ", handle)
	ljm.eWriteName(handle, "FIO2", 1)

	read = threading.Thread(target=read_fn, kwargs={'handle' : handle})
	write = threading.Thread(target=write_fn, kwargs={'handle' : handle})

	read.start()
	write.start()

	read.join()
	write.join()

	print("Closing handle: ", handle)
	ljm.close(handle)