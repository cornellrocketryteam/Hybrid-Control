"""
stream_pwm.py: Basic test for a periodic stream out on a pin (FIO1)
"""
import sys
from time import sleep

from labjack import ljm

def openLJMDevice(deviceType, connectionType, identifier):
    try:
        handle = ljm.open(deviceType, connectionType, identifier)
    except ljm.LJMError:
        print(
            "Error calling ljm.open(" +
            "deviceType=" + str(deviceType) + ", " +
            "connectionType=" + str(connectionType) + ", " +
            "identifier=" + identifier + ")"
        )
        raise

    return handle

def printDeviceInfo(handle):
    info = ljm.getHandleInfo(handle)
    print(
        "Opened a LabJack with Device type: %i, Connection type: %i,\n"
        "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i\n" %
        (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5])
    )

def main():
    scanRate = 1000
    scansPerRead = int(scanRate / 2)
    runTime = 5

    scanListNames = ["STREAM_OUT0"]
    scanList = ljm.namesToAddresses(len(scanListNames), scanListNames)[0]

    print("Beginning...\n")
    handle = openLJMDevice(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")
    printDeviceInfo(handle)

    aNames = ["FIO_STATE"]
    aValues = [
        32386 # 11111101 0000010. This corresponds to FIO1 being targeted
    ]
    numFrames = len(aNames)
    results = ljm.eWriteNames(handle, numFrames, aNames, aValues)

    # ljm.eWriteName(handle, "STREAM_OUT0_TARGET", 2500)  # FIO1 digital outp

    targetAddr = 2500
    streamOutIndex = 0
    samplesToWrite = 512

    writeData = []
    for i in range(samplesToWrite):
        writeData.append(0)
        writeData.append(0)
        writeData.append(0)
        writeData.append(0)
        writeData.append(3)
        writeData.append(3)
        writeData.append(3)
        writeData.append(3)

    print("\nInitializing stream out... \n")
    ljm.periodicStreamOut(handle, streamOutIndex, targetAddr, scanRate, len(writeData), writeData)
    actualScanRate = ljm.eStreamStart(handle, scansPerRead, len(scanList), scanList, scanRate)
    print("Stream started with scan rate of %f Hz\n Running for %d seconds\n" % (scanRate, runTime))
    sleep(runTime)

if __name__ == "__main__":
    main()