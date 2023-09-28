"""
test_stand.py: The model for the Test Stand
"""

from labjack import ljm

class TestStand:

    def __init__(self, handle):
        self.sv_states = [False, False, False, False, False]

        self.mav_state = False
        self.srbv_state = False

        self.mav_dio = 0

        self.handle = handle

    def mav_on(self):
        self._mav_actuate(26.4)

    def mav_off(self):
        self._mav_actuate(72.6)

    def _mav_actuate(self, dc):
        global handle
        roll_value = 242424.24242424243

        config_a = dc * roll_value / 100

        aNames = [
            "DIO_EF_CLOCK0_ROLL_VALUE",
            "DIO_EF_CLOCK0_ENABLE",

            "DIO%i_EF_ENABLE" % self.mav_dio,
            "DIO%i_EF_CONFIG_A" % self.mav_dio,
            "DIO%i_EF_ENABLE" % self.mav_dio,
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

    def sbrv_off(self):
        pass

    def sv_on(self, num):
        pass

    def sv_off(self, num):
        pass

