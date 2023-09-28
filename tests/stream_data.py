"""
File for reading in data from all sensors.

3 September 2023
"""
from datetime import datetime
import sys
from labjack import ljm

sensor_dict = [0.0, 10.0, 0, 2000, "AIN0", "AIN199"]

# CHECK ALL VALUES 
MAX_REQUESTS = 25  # The number of eStreamRead calls that will be performed.
FIRST_AIN_CHANNEL = 0  # 0 = AIN0
NUMBER_OF_AINS = 8 # Streams channels FIRST_AIN_CHANNEL to NUMBER_OF_AINS-1

class sensor():
    def __init__(self, volt_min: float, volt_max: float, val_min: float, val_max: float, pos_channel: str, neg_channel: str) -> None:
        """
        Initializes a sensor with volt_min and volt_max, which are the minimum and maximum voltage outputs
        of the sensor's analog signals, and val_min and val_max, which correspond to the minimum and 
        maximum data values that can be expected from that sensor.

        TO DO: Add gain and offset.
        """
        self.volt_min = volt_min
        self.volt_max = volt_max
        self.val_min = val_min
        self.val_max = val_max
        self.pos_channel = pos_channel
        self.neg_channel = neg_channel


def initialize_sensors():
    """
    Initialize all sensors with their attributes.
    Sensors are initialized as follows:
    s = sensor(voltage min, voltage max, value min, value max, [analog channel, negative analog channel])
    """
    pt1 = sensor(sensor_dict[0], sensor_dict[1], sensor_dict[2], sensor_dict[3], sensor_dict[4], sensor_dict[5])

def linear_interpolation(s: sensor, volt_act: float) -> float:
    """
    Takes a voltage input range, volt_min to volt_max, and scales this to the expected sensor value
    output range, val_min to val_max. Returns the input voltage reading, volt_act, scaled to the
    sensor value output.

    Current method: applying linear scaling formula

    """
    scaled_volt = ((volt_act-s.volt_min)*(s.val_max-s.val_min))/(s.volt_max-s.volt_min) + s.val_min
    return scaled_volt


def analog_read_data():
    """
    Reads data from sensors connected to the LabJack. Uses code from the following script:
    https://github.com/labjack/labjack-ljm-python/blob/master/Examples/More/Stream/stream_sequential_ain.py

    Returns something 
    """
    print("attempting read")
    # Open first found LabJack
    handle = ljm.openS("ANY", "ANY", "ANY")  # Any device, Any connection, Any identifier
    print("found labjack")

    info = ljm.getHandleInfo(handle)
    print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
        "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
        (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

    deviceType = info[0]

    try:
        # Settings for channels 

        # Ensure triggered stream is disabled.
        ljm.eWriteName(handle, "STREAM_TRIGGER_INDEX", 0)

        # Enabling internally-clocked stream.
        ljm.eWriteName(handle, "STREAM_CLOCK_SOURCE", 0)

        # Configure the analog input negative channels, ranges, stream settling
        # times and stream resolution index.
        aNames = ["AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US",
                "STREAM_RESOLUTION_INDEX"]
        aValues = [ljm.constants.GND, 10.0, 0, 0]  # single-ended, +/-10V, 0 (default), 0 (default)
        ljm.eWriteNames(handle, len(aNames), aNames, aValues)

        # Stream configuration
        aScanListNames = ["AIN%i" % i for i in range(FIRST_AIN_CHANNEL, FIRST_AIN_CHANNEL + NUMBER_OF_AINS)]  # Scan list names
        print("\nScan List = " + " ".join(aScanListNames))
        numAddresses = len(aScanListNames)
        aScanList = ljm.namesToAddresses(numAddresses, aScanListNames)[0]
        scanRate = 1000 # CHECK VAL
        scansPerRead = int(scanRate / 2)

        # Configure and start stream
        scanRate = ljm.eStreamStart(handle, scansPerRead, numAddresses, aScanList, scanRate)
        print("\nStream started with a scan rate of %0.0f Hz." % scanRate)

        print("\nPerforming %i stream reads." % MAX_REQUESTS)
        start = datetime.now()
        totScans = 0
        totSkip = 0  # Total skipped samples

        i = 1
        while i <= MAX_REQUESTS: # CHANGE CONDIITOn
            ret = ljm.eStreamRead(handle)

            aData = ret[0]
            scans = len(aData) / numAddresses
            totScans += scans

            # Count the skipped samples which are indicated by -9999 values. Missed
            # samples occur after a device's stream buffer overflows and are
            # reported after auto-recover mode ends.
            curSkip = aData.count(-9999.0)
            totSkip += curSkip

            print("\neStreamRead %i" % i)
            ainStr = ""
            for j in range(0, numAddresses):
                ainStr += "%s = %0.5f, " % (aScanListNames[j], aData[j])
            print("  1st scan out of %i: %s" % (scans, ainStr))
            print("  Scans Skipped = %0.0f, Scan Backlogs: Device = %i, LJM = "
                "%i" % (curSkip / numAddresses, ret[1], ret[2]))
            i += 1

        end = datetime.now()

        print("\nTotal scans = %i" % (totScans))
        tt = (end - start).seconds + float((end - start).microseconds) / 1000000
        print("Time taken = %f seconds" % (tt))
        print("LJM Scan Rate = %f scans/second" % (scanRate))
        print("Timed Scan Rate = %f scans/second" % (totScans / tt))
        print("Timed Sample Rate = %f samples/second" % (totScans * numAddresses / tt))
        print("Skipped scans = %0.0f" % (totSkip / numAddresses))
    except ljm.LJMError:
        ljme = sys.exc_info()[1]
        print(ljme)
    except Exception:
        e = sys.exc_info()[1]
        print(e)

    try:
        print("\nStop Stream")
        ljm.eStreamStop(handle)
    except ljm.LJMError:
        ljme = sys.exc_info()[1]
        print(ljme)
    except Exception:
        e = sys.exc_info()[1]
        print(e)

    # Close handle
    ljm.close(handle)

analog_read_data()

