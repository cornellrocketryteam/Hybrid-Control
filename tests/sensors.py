"""
sensors.py: Basic test for reading from a specific analog channel.

"""

from labjack import ljm

AIN = "AIN127"
AIN_NEGATIVE_CHANNEL = 199 #How to know this val?
AIN_RANGE = 10 #voltage range
AIN_RESOLUTION_INDEX = 0 #idk if i would ever change this
AIN_SETTLING_US = 0 #also dont know if id change this


def read_sensor():
    """
    Reads data from sensors connected to the LabJack. Uses code from the following script:
    https://github.com/labjack/labjack-ljm-python/blob/master/Examples/More/Stream/stream_sequential_ain.py

    Returns something 
    """

    # Open first found LabJack
    handle = ljm.openS("ANY", "ANY", "ANY")  # Any device, Any connection, Any identifier

    info = ljm.getHandleInfo(handle)
    print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
        "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
        (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

    deviceType = info[0]

    # LabJack T7 and other devices configuration

    # AIN0:
    #   Negative channel = single ended (199)
    #   Range: +/-10.0 V (10.0).
    #   Resolution index = Default (0)
    #   Settling, in microseconds = Auto (0)
    names = ["AIN_NEGATIVE_CH", "AIN_RANGE", "AIN_RESOLUTION_INDEX", "AIN_SETTLING_US"]
    aValues = [199, 10, 0, 0] # what does the 199 mean?
    numFrames = len(names)
    ljm.eWriteNames(handle, numFrames, names, aValues)

    print("\nSet configuration:")
    for i in range(numFrames):
        print("    %s : %f" % (names[i], aValues[i]))

    # Setup and call eReadName to read AIN0 from the LabJack.
    name = AIN
    result = ljm.eReadName(handle, name)

    print("\n%s reading : %f V" % (name, result))

    # Close handle
    ljm.close(handle)
    