"""
stream_pwm.py: Unit test for outputting a pseudo PWM output on a DIO pin
"""
import sys
from time import sleep

from labjack import ljm
import ljm_stream_util



def main():
    scanRate = 1000
    scansPerRead = int(scanRate / 2)

    # Number of seconds to stream out waveforms
    runTime = 5

    # The desired stream channels. Up to 4 out-streams can be ran at once
    scanListNames = ["STREAM_OUT0"]
    scanList = ljm.namesToAddresses(len(scanListNames), scanListNames)[0]

    # Only stream out to DIO1 - CONFIRM THIS IS THE RIGHT ADDRESS https://gist.github.com/chrisJohn404/11064514
    targetAddr = 2002

    # Stream out index can only be a number between 0-3
    streamOutIndex = 0
    samplesToWrite = 512

    # Make an arbitrary waveform that increases voltage linearly from 0-2.5V
    writeData = []
    for i in range(samplesToWrite):
        sample = 2.5*i/samplesToWrite
        writeData.append(sample)

    handle = ljm.openS("T7", "ANY", "ANY")


    try :
        print("\nInitializing stream out... \n")
        ljm.periodicStreamOut(handle, streamOutIndex, targetAddr, scanRate, len(writeData), writeData)
        actualScanRate = ljm.eStreamStart(handle, scansPerRead, len(scanList), scanList, scanRate)
        print("Stream started with scan rate of %f Hz\n Running for %d seconds\n" % (scanRate, runTime))
        sleep(runTime)

    except ljm.LJMError:
        ljm_stream_util.prepareForExit(handle)
        raise
    except Exception:
        ljm_stream_util.prepareForExit(handle)
        raise

    ljm_stream_util.prepareForExit(handle)


if __name__ == "__main__":
    main()
