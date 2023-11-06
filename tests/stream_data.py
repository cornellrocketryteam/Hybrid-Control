"""
stream_data.py: File for full sensor implementation. 

Reads and logs sensor data, and scales analog readings to values.

3 November 2023
"""
import time
from labjack import ljm

class Sensor():

    def __init__(self, volt_min: float, volt_max: float, val_min: float, val_max: float) -> None:
        """
        Initializes a sensor with volt_min and volt_max, which are the minimum and maximum voltage outputs
        of the sensor's analog signals, and val_min and val_max, which correspond to the minimum and 
        maximum data values that can be expected from that sensor.
        """
        self.volt_min = volt_min
        self.volt_max = volt_max
        self.val_min = val_min
        self.val_max = val_max
    
    def linear_interpolation(self, volt_act: float) -> float:
        """
        Takes a voltage reading and scales it to the expected sensor value
        output range of the Sensor object using linear interpolation. 
        
        Returns the input voltage reading, volt_act, scaled to the sensor value
        output.
        """
        scaled_volt = ((volt_act - self.volt_min) * (self.val_max - self.val_min)) / (self.volt_max - self.volt_min) + self.val_min
        return scaled_volt
    
    def tc_scale(self, volt_act: float) -> float:
        """
        Takes a voltage reading and scales it to the expected sensor value
        output range of the Sensor object using [INSERT FORMULAS USED].

        Returns the input voltage reading, volt_act, scaled to the sensor value
        output for an RTD.
        """
        pass


def initialize_sensors():
    """
    Initialize all sensors with their attributes.
    Sensors are initialized as follows:
    s = Sensor(voltage min, voltage max, value min, value max)

    TO DO: Add details for reading (positive and negative channels, etc), gain, offset
    """
    pt_1268 = Sensor(0.0, 10.0, 0.0, 2000.0)
    pt_347 = Sensor(0.0, 10.0, 0.0, 3000.0)
    pt_5 = Sensor(0.0, 10.0, 0.0, 1500.0)
    # initialize tcs, fm1, lcs


# AIN 127-120 for PT 1-8, AIN 0-3 for TC 1-4, AIN 60 for FM1, AIN 48-49 for Load Cell 1-2
ain_channels = ["AIN127", "AIN126", "AIN125", "AIN124", "AIN123", "AIN122", "AIN121", "AIN120",
                "AIN0", "AIN1", "AIN2", "AIN3",
                "AIN60",
                "AIN48", "AIN49"]

def ain_read(handle: int, ain_channels: list):
    """
    Streams data from the analog input channels on the LabJack handle as defined in ain_channels.
    """

    try:
        # Open and overwrite log file
        with open("labjack_data.csv", 'w') as file:

            # Add csv header
            file.write(", ".join(ain_channels) + "\n")

            info = ljm.getHandleInfo(handle)
            print("Device Info: {}".format(info))

            # When streaming, negative channels and ranges can be configured for individual analog inputs,
            # but the stream has only one settling time and resolution.

            # Ensure triggered stream is disabled.
            ljm.eWriteName(handle, "STREAM_TRIGGER_INDEX", 0)

            # Enabling internally-clocked stream.
            ljm.eWriteName(handle, "STREAM_CLOCK_SOURCE", 0)

            # Configure Stream settling time
            ljm.eWriteName(handle, "STREAM_SETTLING_US", 0)

            # Configure Stream resolution index
            ljm.eWriteName(handle, "STREAM_RESOLUTION_INDEX", 0)

            # Configure most of the negative channels to single-ended (refrencing GND)
            ljm.eWriteName(handle, "AIN_ALL_NEGATIVE_CH", 199)

            # Configure most of the AIN's ranges
            ljm.eWriteName(handle, "AIN_ALL_RANGE", 10.0)

            # Configure the analog input negative channels and ranges for unique channels
            # Default Configuration: single-ended, +/-10V, 0 Settling US, 0 Resolution Index
            aNames = ["AIN60_NEGATIVE_CH", "AIN60_RANGE",
                    "AIN48_NEGATIVE_CH", "AIN48_RANGE",
                    "AIN49_NEGATIVE_CH", "AIN49_RANGE",]
            aValues = [ljm.constants.GND, 2.4,
                       56, 10.0,
                       57, 10.0,]
            # FIGURE OUT HOW TO CHANGE NEGATIVE CH FOR LOAD CELLS
            # https://labjack.com/pages/support?doc=%2Fapp-notes%2Fsensor-types-app-note%2Fbridge-circuits-app-note%2F
            ljm.eWriteNames(handle, len(aNames), aNames, aValues)

            # Stream configuration
            aScanListNames = ain_channels
            print("Scan List = " + " ".join(aScanListNames))
            numAddresses = len(aScanListNames)
            aScanList = ljm.namesToAddresses(numAddresses, aScanListNames)[0]
            scanRate = 100 # Hz frequency of reading -> TO DO: figure out if it is actually getting all these reads
            scansPerRead = int(scanRate / 2)

            # Stream start
            scanRate = ljm.eStreamStart(handle, scansPerRead, numAddresses, aScanList, scanRate)
            print("Stream started with scan rate: {}".format(scanRate))

            start = time.time()
            totalScans = 0
            totalSamples = 0
            totalSkip = 0  # Total skipped samples [what does this mean]
                           # https://labjack.com/pages/support?doc=%2Fsoftware-driver%2Fljm-users-guide%2Fstreaming-ljm_estreamread-gives-error-1301-ljme_ljm_buffer_full-or-many-9999-values-in-adata-what-can-i-try%2F
            for i in range(0, 10):

                ret = ljm.eStreamRead(handle)
                print("StreamRead\tSamples: {}\tDevice Log: {}\tLJM Log: {}".format(len(ret[0]), ret[1], ret[2]))

                aData = ret[0]
                #DEBUG: This is unecsarry since LJM should return a full scan list at least per read, but a nice scanity check
                if len(aData) % scansPerRead != 0 or len(aData) % numAddresses != 0:
                    raise Exception("Stream Read has an incorrect number of samples: {} {} {}".format(len(aData), scansPerRead, numAddresses))
                totalScans += len(aData) / numAddresses
                totalSamples += len(aData)

                # For each scan list from Stream Read
                for j in range(0, len(aData), numAddresses):
                    # For each sample in the scan list
                    for k in range(j, j+numAddresses):
                        # Check for a skipped sample
                        if aData[k] == -9999.0:
                            totalSkip += 1
                        # Add to file
                        file.write(str(round(aData[k], 3)) + ", ")
                    file.write('\n')

            end = time.time()

            ljm.eStreamStop(handle)
            print("Stream stopped after {} seconds".format(end-start))
            print("Total Scans: {}\tTotal Samples: {}\tTotal Skipped: {}".format(totalScans, totalSamples, totalSkip))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    handle = ljm.openS("T7", "USB", "ANY")  # T7 device, Any connection, Any identifier
    ain_read(handle, ain_channels)
    ljm.close(handle)