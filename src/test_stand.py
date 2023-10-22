"""
test_stand.py: The model for the Test Stand
"""

from labjack import ljm
import threading
from util import Mode, use_labjack

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

        # pressure (PSI) - 8x
        self.pt_pressures = []

        # Thermocouplers (Temp Kelvin) - 4x
        self.tc_temps = []

        # Flowmeter (Gallons per min) - 1x
        self.flowmeter_gpm = -1

        # Load cell (Kilograms) - 2x
        self.load_cell_weights = []

        self.handle = handle

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

    # States

    def default(self) -> None:
        self.mav_off(1)
        self.mav_off(2)
    
    def prefire_purge_tanks(self, on: bool) -> None:
        if on:
            self.sv_on(2)
            self.sv_on(5)
        else:
            self.sv_off(2)
            self.sv_off(5)

    def prefire_purge_engine(self, on: bool) -> None:
        if on:
            self.sv_on(1)
        else:
            self.sv_off(1)

    def fill(self, on: bool) -> None:
        if on:
            self.sv_on(3)
        else:
            self.sv_off(3)

    def supercharge(self) -> None:
        self.sv_on(4)

    def ignition(self) -> None:
        self.sv_on(4)
    
    def firing(self) -> None:
        self.sv_on(4)

        self.mav_on(1)
        self.mav_on(2)
        timer_1 = threading.Timer(150 / 1000, self.mav_off, [1])
        timer_2 = threading.Timer(150 / 1000, self.mav_off, [2])