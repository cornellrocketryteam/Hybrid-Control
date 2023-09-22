"""
test_stand.py: The model for the Test Stand
"""

class TestStand:


    def __init__(self):
        self.sv_states = [False, False, False, False, False]

        self.mav_state = False
        self.srbv_state = False

    def mav_on(self):
        pass

    def mav_off(self):
        pass

    def sbrv_off(self):
        pass

    def sv_on(self, num):
        pass

    def sv_off(self, num):
        pass

