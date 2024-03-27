import wpilib
from lib.subsystem.TorqueSubsystem import TorqueSubsystem
from lib.base.TorqueMode import TorqueMode

class TorqueRobotBase(wpilib.TimedRobot):

    def __init__(self, input: TorqueSubsystem) -> None:
        super().__init__()
        self.subsystems: list[TorqueSubsystem] = []
        self.input = input
    
    def add_subsystem(self, subsystem: TorqueSubsystem) -> None:
        self.subsystems.append(subsystem)
    
    def teleopInit(self) -> None:
        for subsystem in self.subsystems:
            subsystem.initialize(TorqueMode.TELEOP)
    
    def teleopPeriodic(self) -> None:
        self.input.update(TorqueMode.TELEOP)
        for subsystem in self.subsystems:
            subsystem.update(TorqueMode.TELEOP)

    def autonomousInit(self) -> None:
        for subsystem in self.subsystems:
            subsystem.initialize(TorqueMode.AUTO)
    
    def autonomousPeriodic(self) -> None:
        for subsystems in self.subsystems:
            subsystems.update(TorqueMode.AUTO)
    
    def testInit(self) -> None:
        for subsystem in self.subsystems:
            subsystem.initialize(TorqueMode.TEST)
    
    def testPeriodic(self) -> None:
        self.input.update(TorqueMode.TEST)
        for subsystem in self.subsystems:
            subsystem.update(TorqueMode.TEST)