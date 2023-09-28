"""
sv_seq.py: Unit test for actuating a solenoid valve - blocking delay
"""

import time, threading
from labjack import ljm


pwmDIO = 2
dio = "FIO" + str(pwmDIO)

# Do not drop below 100
freq = 1000
dc = 60

def sv_actuate(on):
	global dio, pwmDIO, freq, dc
	state = int(on)
	
	if on:
		print("Turning on")
		ljm.eWriteName(handle, dio, state)
		time.sleep(150 / 1000)

		roll_value = 80_000_000 / freq
		config_a = dc * roll_value / 100

		aNames = [
			"DIO_EF_CLOCK0_ROLL_VALUE",
			"DIO_EF_CLOCK0_ENABLE",

			"DIO%i_EF_ENABLE" % pwmDIO,
			"DIO%i_EF_CONFIG_A" % pwmDIO,
			"DIO%i_EF_ENABLE" % pwmDIO,
		]

		aValues = [
			roll_value,
			1,

			0,
			config_a,
			1
		]
		numFrames = len(aNames)
		results = ljm.eWriteNames(handle, numFrames, aNames, aValues)

	else:
		print("Turning off")
		aNames = ["DIO_EF_CLOCK0_ENABLE", "DIO%i_EF_ENABLE" % pwmDIO]
		aValues = [0, 0]
		numFrames = len(aNames)
		results = ljm.eWriteNames(handle, numFrames, aNames, aValues)

if __name__ == "__main__":
	handle = ljm.openS("T7", "ANY", "ANY")

	sv_actuate(True)
	time.sleep(3)
	sv_actuate(False)

	ljm.close(handle)
