"""
threads.py: A simple test to write to and read from a labjack simultaneously.
"""

from labjack import ljm
import threading
import curses
import time
import csv
import sys

class ThreadTest():
	def __init__(self, handle) -> None:
		names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US"]
		aValues = [199, 10.0, 0, 0]
		numFrames = len(names)
		ljm.eWriteNames(handle, numFrames, names, aValues)

		self.handle = handle
		self.v = 0.0
		self.e = threading.Event()

		self.stdscr = curses.initscr()
		self.stdscr.nodelay(True)
		curses.echo()
		self.stdscr.clear()
		self.stdscr.addstr(0, 0, "ahhhhhhh")

	def read_fn(self) -> None:
		print("tryig to read: ", self.handle)
		#e = threading.Event()

		# Setup and call eReadName to read AIN0 from the LabJack.
		name = "AIN0"
		while True:
			try:
				#print("reading")
				res = ljm.eReadName(self.handle, name) #self.v
				#print(self.v)
				with open("thread_read_test.csv", 'a') as file:
					file.write(str(self.v))
					file.write('\n')
				#print("after read")
			except KeyboardInterrupt:
				self.e.set()
				break


	def write_fn(self) -> None:
		#print("tryign to write: ", self.handle)
		state = True

		#e = threading.Event()

		while True:
			try:
				#print("writng")
				with open("thread_write_test.csv", 'a') as file:
					ljm.eWriteName(self.handle, "FIO2", int(state))
					state = not state
					dict = {"w": self.v}
					self.v += 1
					file.write(str(dict))
					file.write('\n')

				self.update()
				time.sleep(2)
				#print("after write")
			except KeyboardInterrupt:
				self.e.set()
				break
	
	def update(self):
		try: 
			self.stdscr.refresh()

			c = self.get_input()
			if c == 106:
				self.stdscr.addstr(10, 10, "Boy, I sure do love my golden corral")
				self.stdscr.refresh()
			else:
				self.stdscr.clear()


			self.stdscr.addstr(0, 0, str(self.v))

		except KeyboardInterrupt:
			pass
	
	def get_input(self):
		c = self.stdscr.getch()
		print("c: " + str(c))
		return c


if __name__ == "__main__":
	handle = ljm.openS("T7", "ANY", "ANY")
	print("found handle: ", handle)
	ljm.eWriteName(handle, "FIO2", 1)

	t = ThreadTest(handle)

	read = threading.Thread(target=t.read_fn) #, 'val' : v}) #, args=(v))
	write = threading.Thread(target=t.write_fn) #, 'val' : v}) #, args=(v))

	read.start()
	write.start()

	read.join()
	write.join()

	print("Closing handle: ", handle)
	ljm.close(handle)