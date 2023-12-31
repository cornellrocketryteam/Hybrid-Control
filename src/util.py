"""
util.py: Helpful utility objects
"""
from enum import Enum

KEYPAD_0 = 48
KEYPAD_1 = 49
KEYPAD_2 = 50
KEYPAD_3 = 51
KEYPAD_DOT = 46
KEYPAD_DASH = 464
KEY_UPARROW = 259
AMBIENT_TEMP = 20 # TODO update this based on environment
KEYPAD_MODE_BUTTONS = [52, 53, 54, 465, 55, 56, 57] #ASCII codes for numbers + mode buttons
KEY_BACKSPACE = [263, 127, 8]
KEY_ENTER = [343, 10, 13, 459] #Possible ASCII codes for enter key
use_labjack = True

# AIN 127-120 for PT 1-8, AIN 0-2 for TC 1-3, AIN 60 for FM1, AIN 48-49 for Load Cell 1-2
ain_channels = ["AIN127", "AIN126", "AIN125", "AIN124", "AIN123", "AIN122", "AIN121", "AIN120",
                "AIN3", "AIN1", "AIN2",
                "AIN60",
                "AIN48", "AIN49"]

sensor_keys = ["PT1: Supercharge Downstream", "PT2: Engine Chamber", "PT3: ??", "PT4: Purge Tank", "PT5: N2O Tank", "PT6: Run Tank", "PT7: Injector Manifold", "PT8: Purge Downstream",
              "TC1: Run Tank Temp", "TC2: Engine Temp", "TC3: MAV Inlet Temp",
              "FM1",
              "LC1: Thrust", "LC2: Tank Weight"]

sensor_units = ["psi", "psi", "psi", "psi", "psi", "psi", "psi", "psi",
                "*F", "*F", "*F", 
                "GPM", "lbf", "lbf"]

valid_commands = []
for valve in ['sv 1 ', 'sv 2 ', 'sv 3 ', 'sv 4 ', 'sv 5 ', 'mav 1 ']:
    for state in ['on', 'off']:
        valid_commands.append(valve + state)
valid_commands.append('')

class Mode(Enum):
    DEFAULT = 0
    PREFIRE_PURGE_TANKS = 1
    PREFIRE_PURGE_ENGINE = 2
    FILL = 3
    SUPERCHARGE = 4
    POSTFIRE_PURGE_ENGINE = 5
    FIRE = 6


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
        super().__init__(volt_min, volt_max, val_1, val_2)
    
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

    def __init__(self, volt_min: float, volt_max: float, val_1: float, val_2: float, dacref: float) -> None:
        super().__init__(volt_min, volt_max, val_1, val_2)
        self.DACREF = dacref
    
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
        #print(volt_act)
        r_ref = 15000
        alpha = 0.00392 # Ohms/Ohms/ºC
        r_nom = 100

        r_rtd = (r_ref * (self.DACREF - volt_act))/(volt_act)
        delta_tempC = (1/alpha) * ((r_rtd/r_nom) - 1)
        #temp = AMBIENT_TEMP + delta_temp
        return delta_tempC *(9/5) + 32 #return in *F

class LC(Sensor):

    def __init__(self, volt_min: float, volt_max: float, val_1: float, val_2: float) -> None:
        super().__init__(volt_min, volt_max, val_1, val_2)

    def scale(self, volt_act: float) -> float:
        """
        Takes a volatge reading and scales it to the expected load cell output range.
        """
        x = volt_act
        m = self.val_1
        b = self.val_2

        return 1000 * ((m * x) + b)

def state_onoff(state):
    if state:
        return 'off'
    else:
        return 'on'
    
def nameofSV(num):
    if num == 1:
        return "N2 Engine Purge Solenoid"
    elif num == 2:
        return "N2 Tank/Line Purge Solenoid"
    elif num == 3:
        return "N2O Fill Solenoid"
    elif num == 4:
        return "N2 Supercharge Solenoid"
    elif num == 5:
        return "Tank Vent Solenoid"