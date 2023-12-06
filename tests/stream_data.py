"""
stream_data.py: File for full sensor implementation. 

Reads and logs sensor data, and scales analog readings to values.

3 November 2023
"""
import time
from labjack import ljm

class Sensor():

    def __init__(self, volt_min: float, volt_max: float, val_1: float, val_2: float) -> None:
        """
        Initializes a sensor with volt_min and volt_max, which are the minimum and maximum voltage outputs
        of the sensor's analog signals, and val_1 and val_2, which correspond to the minimum and 
        maximum data values that can be expected from that sensor for pressure transducers and
        RTDs or a slope and y-intercept for load cells.
        """
        self.volt_min = volt_min
        self.volt_max = volt_max
        self.val_1 = val_1
        self.val_2 = val_2

class PT_FM(Sensor):

    def __init__(self, volt_min: float, volt_max: float, val_1: float, val_2: float) -> None:
        super().__init__(self, volt_min, volt_max, val_1, val_2)
    
    def scale(self, volt_act: float) -> float:
        """
        Takes a voltage reading and scales it to the expected sensor value
        output range of a pressure transducer using linear interpolation. 
        Used for pressure transducers and flowmeter.
        
        Returns the input voltage reading, volt_act, scaled to the sensor value
        output.
        """
        scaled_volt = ((volt_act - self.volt_min) * (self.val_2 - self.val_1)) / (self.volt_max - self.volt_min) + self.val_1
        
        return scaled_volt

class TC(Sensor):

    def __init__(self, volt_min: float, volt_max: float, val_1: float, val_2: float) -> None:
        super().__init__(self, volt_min, volt_max, val_1, val_2)
    
    def scale(self, volt_act: float) -> float:
        """
        Takes a voltage reading and scales it to the expected RTD value
        output range of the Sensor object using [INSERT FORMULAS USED].
        Resistance constants set in this function are all in Ohms;
        voltage constants are all in Volts.

        Returns the input voltage reading, volt_act, scaled to the sensor value
        output for an RTD.
        """
        # constants
        r_ref = 15000
        v_c = 5
        r_s = 50
        alpha = 0.00392 # Ohms/Ohms/ºC

        # calculate resistance of RTD using [insert formula]
        r_rtd = r_ref * ((v_c/volt_act) - 1) - r_s
        # calculate temperature using [insert formula]
        temp = (1/alpha) * ((r_rtd/r_ref) - 1)

        return temp

class LC(Sensor):

    def __init__(self, volt_min: float, volt_max: float, val_1: float, val_2: float) -> None:
        super().__init__(self, volt_min, volt_max, val_1, val_2)

    def scale(self, volt_act: float) -> float:
        """
        Takes a volatge reading and scales it to the expected load cell output range.
        """
        x = volt_act
        m = self.val_1
        b = self.val_2

        return 1000 * ((m * x) + b)


def initialize_sensors() -> dict:
    """
    Initialize all sensors with their attributes.
    Sensors are initialized as follows:
    s = Sensor(voltage min, voltage max, value 1, value 2)

    Returns a dictionary of initialized sensors with indices as keys.

    TO DO: Add details for reading (positive and negative channels, etc), gain, offset
    """
    pt2000 = PT_FM(0.0, 10.0, 0.0, 2000.0)
    pt3000 = PT_FM(0.0, 10.0, 0.0, 3000.0)
    pt1500 = PT_FM(0.0, 10.0, 0.0, 1500.0)
    tc = TC(0.0, 10.0, 1.0, 200.0)
    fm = PT_FM(1.72, 10.32, 2.5, 29.0)
    lc1000 = LC(0.0, 0.0036, 31.27993035, -0.2654580671)
    lc2000 = LC(0.0, 0.0036, 60.25906654, -0.02513497142)


    return {0: pt2000, 1: pt2000, 2: pt3000, 3: pt3000, 4: pt1500, 5: pt2000, 6: pt3000, 7: pt2000,
            8: tc, 9: tc, 10: tc,
            11: fm,
            12: lc1000, 13: lc2000}


# AIN 127-120 for PT 1-8, AIN 0-2 for TC 1-3, AIN 60 for FM1, AIN 48-49 for Load Cell 1-2
ain_channels = ["AIN127", "AIN126", "AIN125", "AIN124", "AIN123", "AIN122", "AIN121", "AIN120",
                "AIN0", "AIN1", "AIN2",
                "AIN60",
                "AIN48", "AIN49"]

sensor_keys = ["PT1", "PT2", "PT3", "PT4", "PT5", "PT6", "PT7", "PT8",
              "TC1", "TC2", "TC3",
              "FM1",
              "LC1", "LC2"]

def ain_read(handle: int, ain_channels: list) -> None:
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
                    dataList = aData
                    # For each sample in the scan list
                    for k in range(j, j+numAddresses):
                        # Check for a skipped sample

                        # aData is a list
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
    sensor_list = initialize_sensors()
    ain_read(handle, ain_channels)
    ljm.close(handle)