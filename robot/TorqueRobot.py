import wpilib
from lib.subsystem.TorqueSubsystem import Subsystem

class TorqueRobotBase(wpilib.TimedRobot):

    def __init__(self) -> None:
        super().__init__()
        self.subsystems: list[Subsystem] = []
    
    def add_subsystem(self, subsystem: Subsystem) -> None:
        self.subsystems.append(subsystem)
    
    def robotInit(self) -> None:
        for subsystem in self.subsystems:
            subsystem.initialize()
    
    def robotPeriodic(self) -> None:
        for subsystem in self.subsystems:
            subsystem.update()