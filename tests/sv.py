"""
sv.py: Unit test for actuating a solenoid valve
"""

import time, threading
from labjack import ljm


pwmDIO = 2
dio = "FIO" + str(pwmDIO)

# Do not drop below 100
freq = 1000
dc = 60

def sv_pwm():
	global pwmDIO, freq, dc

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

def sv_actuate(on):
	global dio, pwmDIO
	state = int(on)
	print(state)
	ljm.eWriteName(handle, dio, state)

	if on:
		timer.start()
	else:
		aNames = [
			"DIO%i_EF_ENABLE" % pwmDIO,
		]
		aValues = [
			0
		]
		numFrames = len(aNames)
		results = ljm.eWriteNames(handle, numFrames, aNames, aValues)


if __name__ == "__main__":
	handle = ljm.openS("T7", "ANY", "ANY")

	timer = threading.Timer(150 / 1000, sv_pwm)

	sv_actuate(True)
	time.sleep(3)
	sv_actuate(False)

	ljm.close(handle)

