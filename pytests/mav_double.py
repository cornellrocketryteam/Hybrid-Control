"""
mav.py: Unit test for controlling a mechanically actuated valve
"""

import time
from labjack import ljm


roll_value = 242424.24242424243

def mav_actuate(dc, pwmDIO):
    global roll_value

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

if __name__ == "__main__":
    handle = ljm.openS("T7", "ANY", "ANY")

    pwmDIO_0 = 2
    pwmDIO_1 = 3
    
    mav_actuate(26.4, pwmDIO_0)
    mav_actuate(26.4, pwmDIO_1)

    #mav_actuate(72.6, pwmDIO_1)

    time.sleep(3.0)

    mav_actuate(72.6, pwmDIO_0)
    mav_actuate(72.6, pwmDIO_1)

    #mav_actuate(26.4, pwmDIO_1)
    
    ljm.close(handle)




