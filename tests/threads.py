"""
threads.py: A simple test to write to and read from a labjack simultaneously.
"""

from labjack import ljm
import threading
import time
import csv


def read_fn(handle):
	print("tryig to read: ", handle)
	names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US"]
	aValues = [199, 10.0, 0, 0]
	numFrames = len(names)
	ljm.eWriteNames(handle, numFrames, names, aValues)

	e = threading.Event()
	global v

	# Setup and call eReadName to read AIN0 from the LabJack.
	name = "AIN0"
	while True:
		try:
			print("reading")
			result = ljm.eReadName(handle, name)
			print(v)
			time.sleep(1)
			print("after read")
		except KeyboardInterrupt:
			e.set()
			break


def write_fn(handle):
	print("tryign to write: ", handle)
	state = True

	e = threading.Event()
	global v

	while True:
		try:
			print("writng")
			with open("thread_test.csv", 'a') as file:
				result = ljm.eWriteName(handle, "FIO2", int(state))
				state = not state
				file.write(str(v))
				file.write('\n')
			v += 1
			print("val changeed")
			time.sleep(1)
			print("after write")
		except KeyboardInterrupt:
			e.set()
			break


if __name__ == "__main__":
	handle = ljm.openS("T7", "ANY", "ANY")
	print("found handle: ", handle)
	ljm.eWriteName(handle, "FIO2", 1)

	v = 0

	read = threading.Thread(target=read_fn, kwargs={'handle' : handle}) #, 'val' : v}) #, args=(v))
	write = threading.Thread(target=write_fn, kwargs={'handle' : handle}) #, 'val' : v}) #, args=(v))

	read.start()
	write.start()

	read.join()
	write.join()

	print("Closing handle: ", handle)
	ljm.close(handle)