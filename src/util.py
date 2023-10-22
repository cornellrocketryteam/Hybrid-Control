"""
util.py: Helpful utility objects
"""
from enum import Enum

class Mode(Enum):
    DEFAULT = 0
    PREFIRE_PURGE_TANKS = 1
    PREFIRE_PURGE_ENGINE = 2
    FILL = 3
    SUPERCHARGE = 4
    IGNITION = 5
    FIRE = 6

use_labjack = False