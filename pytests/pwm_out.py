"""
pwm_out.py: Basic test for configuring PWM on a DIO pin
"""

import time
from labjack import ljm

pwmDIO = 2

def pwm_out(freq, dc):
	global pwmDIO

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


def pwm_off():
	global pwmDIO

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

	pwm_out(300, 25)
	time.sleep(3)
	pwm_off()
	# time.sleep(5)
	# pwm_out(300, 75)
	# time.sleep(5)

	ljm.close(handle)

