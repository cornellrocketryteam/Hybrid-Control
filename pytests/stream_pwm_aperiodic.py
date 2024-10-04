"""
stream_pwm.py: Basic test for an aperiodic stream out on a pin (FIO1)
"""
import sys
from time import sleep

from labjack import ljm

def main():
    scanRate = 70
    scansPerRead = 1
    runTime = 5

    scanListNames = ["STREAM_OUT0"]
    scanList = ljm.namesToAddresses(len(scanListNames), scanListNames)[0]

    print("Beginning...\n")
    handle = ljm.openS("T7", "ANY", "ANY")

    targetAddr = 2500
    streamOutIndex = 0

    err = ljm.initializeAperiodicStreamOut(
        handle,
        streamOutIndex,
        targetAddr,
        scanRate
    )

    aNames = ["FIO_STATE"]
    aValues = [
        32386 # 11111101 0000010. This corresponds to FIO1 being targeted
    ]
    numFrames = len(aNames)
    results = ljm.eWriteNames(handle, numFrames, aNames, aValues)
    
    samplesToWrite = 200

    writeData = []
    for i in range(samplesToWrite):
        writeData.append(0)
        writeData.append(3)

    actualScanRate = ljm.eStreamStart(handle, scansPerRead, len(scanList), scanList, scanRate)

    ljm.writeAperiodicStreamOut(handle, streamOutIndex, len(writeData), writeData)
    
    sleep(runTime)

if __name__ == "__main__":
    main()