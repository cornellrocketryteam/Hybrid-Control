"""
File for reading in data from all sensors.

3 September 2023
"""
sensor_list = []

class sensor():
    def __init__(volt_min, volt_max, val_min, val_max):
        self.volt_min = volt_min
        self.volt_max = volt_max
        self.val_min = val_min
        self.val_max = val_max


def linear_interpolation(s: sensor, volt_act: float) -> float:
    """
    Takes a voltage input range, volt_min to volt_max, and scales this to the expected sensor value
    output range, val_min to val_max. Returns the input voltage reading, volt_act, scaled to the
    sensor value output.
    """
    pass

def read_data():
    """
    Reads data from sensors connected to the LabJack.
    """
    pass

def initialize_sensors():
    """
    Initialize all sensors with their attributes.
    """