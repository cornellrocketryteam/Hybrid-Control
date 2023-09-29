"""
test_stand.py: The model for the Test Stand
"""

from labjack import ljm
import threading

class TestStand:

    def __init__(self, handle: int) -> None:
        # Consider a class
        self.sv_states = [False, False, False, False, False]
        self.sv_dio = [1, 0, 2, 3, 4]
        self.sv_freq = 1000
        self.sv_dc = 60
        self.sv_timers = []

        for i in range(5):
            self.sv_timers.append(threading.Timer(150 / 1000, self._sv_pwm, [i]))

        self.mav_states = [False, False]
        self.mav_dio = [5, 6]

        self.handle = handle

    def mav_on(self, num: int) -> None:
        self.mav_states[num - 1] = True
        self._mav_actuate(num, 26.4)

    def mav_off(self, num: int) -> None:
        self.mav_states[num - 1] = False
        self._mav_actuate(num, 72.6)

    def _mav_actuate(self, num: int, dc: float) -> None:
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
        pwmDIO = self.sv_states[num - 1]
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
        self.sv_states[num - 1] = True
        dio = "FIO" + str(self.sv_dio[num - 1])

        ljm.eWriteName(self.handle, dio, 1)
        self.sv_timers[num - 1].start()
        
    def sv_off(self, num: int) -> None:
        self.sv_states[num - 1] = False
        dio = "FIO" + str(self.sv_dio[num - 1])

        aNames = ["DIO_EF_CLOCK0_ENABLE", "DIO%i_EF_ENABLE" % self.sv_dio[num - 1]]
        aValues = [0, 0]
        numFrames = len(aNames)
        results = ljm.eWriteNames(self.handle, numFrames, aNames, aValues)
        ljm.eWriteName(self.handle, dio, 0)
