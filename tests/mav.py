"""
mav.py: Unit test for controlling a mechanically actuated valve
"""

import time
from labjack import ljm


# Uses DIO0.
# 10 kHz PWM at a 25% duty cycle

def mav_on():
    pwmDIO = 0
    aNames = [
        "DIO_EF_CLOCK0_ROLL_VALUE",
        "DIO_EF_CLOCK0_ENABLE",
        "DIO%i_EF_ENABLE" % pwmDIO,
        "DIO%i_EF_INDEX" % pwmDIO,
        "DIO%i_EF_CONFIG_A" % pwmDIO,
        "DIO%i_EF_ENABLE" % pwmDIO,
    ]
    aValues = [
        170000,
        0,
        0,
        0,
        2000,
        1,
    ]
    
    numFrames = len(aNames)
    results = ljm.eWriteNames(handle, numFrames, aNames, aValues)

def mav_off():
    pwmDIO = 0
    aNames = ["DIO_EF_CLOCK0_ENABLE", "DIO%i_EF_ENABLE" % pwmDIO]
    aValues = [0, 0]
    numFrames = len(aNames)
    results = ljm.eWriteNames(handle, numFrames, aNames, aValues)

if __name__ == "__main__":
    handle = ljm.openS("T7", "ANY", "ANY")
    mav_on()
    time.sleep(3.0)
    #mav_off()
    ljm.close(handle)
