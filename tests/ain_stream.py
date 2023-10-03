"""
Streams from multiple AIN channels.
"""
from datetime import datetime
import sys
from labjack import ljm


# AIN 127-120 for PT 1-8, AIN 0-3 for TC 1-4, AIN 60 for FM1, AIN 48-49 for Load Cell 1-2
ain_channels = ["AIN127", "AIN126", "AIN125", "AIN124", "AIN123", "AIN122", "AIN121", "AIN120",
"AIN0", "AIN1", "AIN2", "AIN3", "AIN60", "AIN48", "AIN49"]

def ain_read(handle: int, ain_channels: list) -> str:
    """
    Streams data from the analog input channels on the LabJack handle as defined in ain_channels.
    Returns a dict with the AIN channel as a key and the voltage reading as a value.
    """

    # Deletes the contents currently in the csv file
    f = open('labjack_data.csv', 'w')
    f.close()

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
        aNames = ["AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX",
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX",
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX",
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"
                  "AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"]
        aValues = [ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 10.0, 0, 0,
                   ljm.constants.GND, 2.4, 0, 0,
                   56, 10.0, 0, 0,
                   57, 10.0, 0, 0,]  # single-ended, +/-10V, 0 (default), 0 (default) #FIGURE OUT HOW TO CHANGE NEGATIVE CH FOR LOAD CELLS
        ljm.eWriteNames(handle, len(aNames), aNames, aValues)

        # Stream configuration
        aScanListNames = ain_channels
        #print("\nScan List = " + " ".join(aScanListNames))
        numAddresses = len(aScanListNames)
        aScanList = ljm.namesToAddresses(numAddresses, aScanListNames)[0]
        scanRate = 100 # Hz frequency of reading
        scansPerRead = int(scanRate / 2)

        # Configure and start stream
        #print("Stream Start")
        scanRate = ljm.eStreamStart(handle, scansPerRead, numAddresses, aScanList, scanRate)
        #print("\nPerforming %i stream reads." % MAX_REQUESTS)
        start = datetime.now()
        totScans = 0
        totSkip = 0  # Total skipped samples [what does this mean]

        stream = 0
        while stream < 25:
            
            ret = ljm.eStreamRead(handle)
            aData = ret[0]
            scans = len(aData) / numAddresses
            totScans += scans

            # print("\neStreamRead %i" % i) # Prints each stream instance from stream 1 to MAX_REQUESTS
            ainDict = {}
            for j in range(0, numAddresses):
                ainDict[aScanListNames[j]] = round(aData[j], 3)
            f = open('labjack_data.csv', 'a')
            f.write(str(ainDict) + "\n")
            f.close()
            #print("  1st scan out of %i: %s" % (scans, ainStr))
            #print("  Scans Skipped = %0.0f, Scan Backlogs: Device = %i, LJM = "
            #      "%i" % (curSkip / numAddresses, ret[1], ret[2]))
            
            stream += 1

        f.close()
        end = datetime.now()

    except ljm.LJMError:
        ljme = sys.exc_info()[1]
        print(ljme)
    except Exception:
        e = sys.exc_info()[1]
        print(e)

    try:
        #print("\nStop Stream")
        ljm.eStreamStop(handle)
    except ljm.LJMError:
        ljme = sys.exc_info()[1]
        print(ljme)
    except Exception:
        e = sys.exc_info()[1]
        print(e)



if __name__ == "__main__":
    handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier
    ain_read(handle, ain_channels)
    ljm.close(handle)
