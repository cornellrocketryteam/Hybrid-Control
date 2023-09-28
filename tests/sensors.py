"""
sensors.py: Basic test for reading from a specific analog channel.

"""

from labjack import ljm

pt1 = [0.0, 10.0, 0, 2000]
# pt2 = [0.0, 10.0, 0, 2000, ["AIN127", 199]]
# pt3 = [0.0, 10.0, 0, 3000, ["AIN127", 199]]
# pt4 = [0.0, 10.0, 0, 3000, ["AIN127", 199]]
# pt5 = [0.0, 10.0, 0, 1500, ["AIN127", 199]]
# pt6 = [0.0, 10.0, 0, 2000, ["AIN127", 199]]
# pt7 = [0.0, 10.0, 0, 1500, ["AIN127", 199]]
# pt8 = [0.0, 10.0, 0, 2000, ["AIN127", 199]]

ain = "AIN2"
ain_negative_ch = 199 # 199 for GND
ain_range = pt1[1] # voltage range

AIN_RESOLUTION_INDEX = 0 # idk if i would ever change this
AIN_SETTLING_US = 0 # also dont know if id change this


def read_sensor():
    """
    Reads data from a single analog channel on the LabJack. Uses code from the following script:
    https://github.com/labjack/labjack-ljm-python/blob/master/Examples/More/AIN/single_ain_with_config.py
    """

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
    aValues = [ain_negative_ch, ain_range, AIN_RESOLUTION_INDEX, AIN_SETTLING_US]
    numFrames = len(names)
    ljm.eWriteNames(handle, numFrames, names, aValues)

    print("\nSet configuration:")
    for i in range(numFrames):
        print("    %s : %f" % (names[i], aValues[i]))

    # Setup and call eReadName to read AIN0 from the LabJack.
    name = ain
    result = ljm.eReadName(handle, name)

    print("\n%s reading : %f V" % (name, result))


if __name__ == "__main__":
    handle = ljm.openS("T7", "ANY", "ANY")
    read_sensor()
    ljm.close(handle)

    