from enum import Enum

class TorqueMode(Enum):
    DISABLED = 0
    TELEOP = 1
    AUTO = 2
    TEST = 3
    SIM = 4
    ERROR = 5