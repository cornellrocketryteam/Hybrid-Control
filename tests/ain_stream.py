"""
Streams from multiple AIN channels.
"""
from datetime import datetime
import sys

from labjack import ljm

# Open first found LabJack
handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier

# AIN 127-120 for PT 1-8, AIN 0-3 for TC 1-4, AIN 60 for FM1, AIN 48-49 for Load Cell 1-2
ain_channels = ["AIN127", "AIN126", "AIN125", "AIN124", "AIN123", "AIN122", "AIN121", "AIN120",
"AIN0", "AIN1", "AIN2", "AIN3", "AIN60", "AIN48", "AIN49"]

def ain_read(handle: int, ain_channels: list) -> str:
    """
    Streams data from the analog input channels on the LabJack handle as defined in ain_channels.
    Returns a dict with the AIN channel as a key and the voltage reading as a value.
    """

    f = open('labjack_data.csv', 'w')
    f.close()

    f = open('labjack_data.csv', 'a')
    
    info = ljm.getHandleInfo(handle)
    deviceType = info[0]


    try:
        # When streaming, negative channels and ranges can be configured for
        # individual analog inputs, but the stream has only one settling time and
        # resolution.
        
        # T7 and other devices configuration

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
        aScanListNames = ain_channels
        #print("\nScan List = " + " ".join(aScanListNames))
        numAddresses = len(aScanListNames)
        aScanList = ljm.namesToAddresses(numAddresses, aScanListNames)[0]
        scanRate = 100 # Hz frequency of reading
        scansPerRead = int(scanRate / 2)

        # Configure and start stream
        print("Stream Start")
        scanRate = ljm.eStreamStart(handle, scansPerRead, numAddresses, aScanList, scanRate)

        #print("\nPerforming %i stream reads." % MAX_REQUESTS)
        start = datetime.now()
        totScans = 0
        totSkip = 0  # Total skipped samples [what does this mean]

        stream = True
        while stream:
            ret = ljm.eStreamRead(handle)

            aData = ret[0]
            scans = len(aData) / numAddresses
            totScans += scans

            # Count the skipped samples which are indicated by -9999 values. Missed
            # samples occur after a device's stream buffer overflows and are
            # reported after auto-recover mode ends.
            curSkip = aData.count(-9999.0)
            totSkip += curSkip

            # print("\neStreamRead %i" % i) # Prints each stream instance from stream 1 to MAX_REQUESTS
            ainStr = ""
            for j in range(0, numAddresses):
                ainStr += "%s = %0.5f, " % (aScanListNames[j], aData[j])
            print(ainStr)
            f.write(ainStr + "\n")
            stream = ainStr
            #print("  1st scan out of %i: %s" % (scans, ainStr))
            #print("  Scans Skipped = %0.0f, Scan Backlogs: Device = %i, LJM = "
            #      "%i" % (curSkip / numAddresses, ret[1], ret[2]))
            
            # INCLUDE stream = False CONDITION

        end = datetime.now()

        """
        print("\nTotal scans = %i" % (totScans))
        tt = (end - start).seconds + float((end - start).microseconds) / 1000000
        print("Time taken = %f seconds" % (tt))
        print("LJM Scan Rate = %f scans/second" % (scanRate))
        print("Timed Scan Rate = %f scans/second" % (totScans / tt))
        print("Timed Sample Rate = %f samples/second" % (totScans * numAddresses / tt))
        print("Skipped scans = %0.0f" % (totSkip / numAddresses))
        """
        return stream
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


ain_read(handle, ain_channels)
# Close handle
ljm.close(handle)
