"""
pwm_out.py: Basic test for configuring PWM on a DIO pin
"""

import time
from labjack import ljm

# Frequency (Hz)
frequency = 50

# Duty cycle (%)
duty_cycle = 25

pwm_DIO = 0

def pwm_out():
	global frequency, duty_cycle, pwm_DIO

	roll_value = 80_000_000 / frequency
	config_a = (duty_cycle * roll_value) / 100

	aNames = [
        "DIO_EF_CLOCK0_ROLL_VALUE",
        "DIO_EF_CLOCK0_ENABLE",
        "DIO%i_EF_ENABLE" % pwmDIO,
        "DIO%i_EF_INDEX" % pwmDIO,
        "DIO%i_EF_CONFIG_A" % pwmDIO,
        "DIO%i_EF_ENABLE" % pwmDIO,
    ]

if __name__ == "__main__":
	handle = ljm.openS("T7", "ANY", "ANY")
    time.sleep(5)
	ljm.close(handle)
