"""
threads.py: A simple test to write to and read from a labjack simultaneously.
"""
from labjack import ljm
import threading
import time



def read_fn():
	names = ["AIN_NEGATIVE_CH", "AIN_RANGE", "AIN_RESOLUTION_INDEX", "AIN_SETTLING_US"]
	aValues = [199, 10.0, 0, 0]
	numFrames = len(names)
	ljm.eWriteNames(handle, numFrames, names, aValues)

	print("\nSet configuration:")
	for i in range(numFrames):
		print("    %s : %f" % (names[i], aValues[i]))

	# Setup and call eReadName to read AIN0 from the LabJack.
	name = "AIN0"
	while True:
		result = ljm.eReadName(handle, name)

def write_fn():
	state = True
	while True:
		result = ljm.eWriteName(handle, "FIO2", int(state))
		state = not state
		time.sleep(1)


if __name__ == "__main__":
	handle = ljm.openS("T7", "ANY", "ANY")

	read = threading.Thread(target=read_fn)
	write = threading.Thread(target=write_fn)

	read.start()
	write.start()

	read.join()
	write.join()
	
	ljm.close(handle)



