"""
test_stand.py: The model for the Test Stand
"""

from labjack import ljm
import threading
from util import Mode, PT_FM, TC, LC, use_labjack, ain_channels
from typing import List
import time

class TestStand:

    def __init__(self, handle: int) -> None:
        # Consider a class
        self.sv_states = [False, False, False, False, False]
        self.sv_dio = [1, 0, 2, 3, 4]
        self.sv_freq = 1000
        self.sv_dc = 10
        self.sv_timers = []

        self.temp_timer = threading.Timer(150 / 1000, self._sv_pwm, [2])
        for i in range(5):
            self.sv_timers.append(threading.Timer(150 / 1000, self._sv_pwm, [i]))

        self.mav_states = [False, False]
        self.mav_dio = [5, 6]

        # sensor dict
        self.sensor_dict = self.initialize_sensors()

        # pressure (PSI) - 8x
        self.pt_pressures = []

        # Thermocouplers (Temp Kelvin) - 4x
        self.tc_temps = []

        # Flowmeter (Gallons per min) - 1x
        self.flowmeter_gpm = -1

        # Load cell (Kilograms) - 2x
        self.load_cell_weights = []

        self.handle = handle

        self.awaited_mode = -1

        self.tanks_purging = False
        self.engine_purging = False
        self.filling = False

    def mav_on(self, num: int) -> None:
        if not self.mav_states[num - 1]:
            if num == 1:
                self.mav_states[num - 1] = True
                self._mav_actuate(num, 26.4)
            else:
                self.mav_states[num - 1] = True
                self._mav_actuate(num, 72.6)

    def mav_off(self, num: int) -> None:
        if self.mav_states[num - 1]:
            if num == 1:
                self.mav_states[num - 1] = False
                self._mav_actuate(num, 72.6)
            else:
                self.mav_states[num - 1] = False
                self._mav_actuate(num, 26.4)

    def _mav_actuate(self, num: int, dc: float) -> None:
        if not use_labjack:
            return
        
        pwmDIO = self.mav_dio[num - 1]
        roll_value = 242424.24242424243

        config_a = dc * roll_value / 100

        aNames = [
            "DIO_EF_CLOCK0_ROLL_VALUE",
            "DIO_EF_CLOCK0_ENABLE",

            "DIO%i_EF_ENABLE" % pwmDIO,
            "DIO%i_EF_CONFIG_A" % pwmDIO,
            "DIO%i_EF_ENABLE" % pwmDIO,
        ]

        aValues = [
            roll_value,
            1,

            0,
            config_a,
            1
        ]
        numFrames = len(aNames)
        results = ljm.eWriteNames(self.handle, numFrames, aNames, aValues)

    def _sv_pwm(self, num: int) -> None:
        # TODO: Needs some fixing for indices
        pwmDIO = self.sv_dio[num - 1]
        #pwmDIO = 2
        roll_value = 80_000_000 / self.sv_freq
        config_a = self.sv_dc * roll_value / 100

        aNames = [
            "DIO_EF_CLOCK0_ROLL_VALUE",
            "DIO_EF_CLOCK0_ENABLE",

            "DIO%i_EF_ENABLE" % pwmDIO,
            "DIO%i_EF_CONFIG_A" % pwmDIO,
            "DIO%i_EF_ENABLE" % pwmDIO,
        ]

        aValues = [
            roll_value,
            1,

            0,
            config_a,
            1
        ]
        numFrames = len(aNames)
        results = ljm.eWriteNames(self.handle, numFrames, aNames, aValues)

    def sv_on(self, num: int) -> None:
        if not self.sv_states[num - 1]:
            self.sv_states[num - 1] = True

            if not use_labjack:
                return
            
            dio = "FIO" + str(self.sv_dio[num - 1])

            ljm.eWriteName(self.handle, dio, 1)
            self.sv_timers[num - 1].start()
            # Create new timer?
            #self.temp_timer.start()
        
    def sv_off(self, num: int) -> None:
        if self.sv_states[num - 1]:
            self.sv_states[num - 1] = False

            if not use_labjack:
                return
            
            dio = "FIO" + str(self.sv_dio[num - 1])
            aNames = ["DIO_EF_CLOCK0_ENABLE", "DIO%i_EF_ENABLE" % self.sv_dio[num - 1]]
            aValues = [0, 0]
            numFrames = len(aNames)
            results = ljm.eWriteNames(self.handle, numFrames, aNames, aValues)
            ljm.eWriteName(self.handle, dio, 0)

    def set_sv_states(self, states: List[bool]) -> None:
        for i in range(5):
            if states[i]:
                self.sv_on(i+1)
            else:
                self.sv_off(i+1)

    # Modes

    def confirm_mode(self, mode: Mode) -> None:
        if mode == Mode.DEFAULT:
            self.default()
        elif mode == Mode.PREFIRE_PURGE_TANKS:
            self.prefire_purge_tanks()
        elif mode == Mode.PREFIRE_PURGE_ENGINE:
            self.prefire_purge_engine()
        elif mode == Mode.FILL:
            self.fill()
        elif mode == Mode.SUPERCHARGE:
            self.supercharge()
        elif mode == Mode.IGNITION:
            self.ignition()
        elif mode == Mode.FIRE:
            self.fire()

    def default(self) -> None:
        self.set_sv_states([False] * 5)

        self.mav_off(1)
        self.mav_off(2)
    
    def prefire_purge_tanks(self) -> None:
        if not self.tanks_purging:
            self.set_sv_states([False, True, False, False, True])
        else:
            self.set_sv_states([False] * 5)

    def prefire_purge_engine(self) -> None:
        if not self.engine_purging:
            self.set_sv_states([True, False, False, False, False])
        else:
            self.set_sv_states([False] * 5)

    def fill(self) -> None:
        if not self.filling:
            self.set_sv_states([False, False, True, False, False])
        else:
            self.set_sv_states([False] * 5)

    def supercharge(self) -> None:
        self.set_sv_states([False, False, False, True, False])

    def ignition(self) -> None:
        self.set_sv_states([False, False, False, True, False])
        # Igniter
    
    def fire(self) -> None:
        self.set_sv_states([False, False, False, True, False])

        self.mav_on(1)
        self.mav_on(2)
        timer_1 = threading.Timer(150 / 1000, self.mav_off, [1])
        timer_2 = threading.Timer(150 / 1000, self.mav_off, [2])

    # Sensors
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
    
    def ain_read(handle: int) -> None:
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
