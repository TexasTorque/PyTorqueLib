import wpilib
from lib.subsystem.TorqueSubsystem import TorqueSubsystem
from lib.base.TorqueMode import TorqueMode
from auto.automanager import AutoManager

class TorqueRobotBase(wpilib.TimedRobot):

    def __init__(self, input: TorqueSubsystem, automanager: AutoManager) -> None:
        super().__init__()
        self.subsystems: list[TorqueSubsystem] = []
        self.input = input
        self.automanager = automanager
    
    def add_subsystem(self, subsystem: TorqueSubsystem) -> None:
        self.subsystems.append(subsystem)

    def robotInit(self) -> None:
        self.automanager.load_paths()
    
    def teleopInit(self) -> None:
        for subsystem in self.subsystems:
            subsystem.initialize(TorqueMode.TELEOP)
    
    def teleopPeriodic(self) -> None:
        self.input.update(TorqueMode.TELEOP)
        for subsystem in self.subsystems:
            subsystem.update(TorqueMode.TELEOP)
        for subsystem in self.subsystems:
            subsystem.clean(TorqueMode.TELEOP)

    def autonomousInit(self) -> None:
        self.automanager.choose_current_sequence()
        for subsystem in self.subsystems:
            subsystem.initialize(TorqueMode.AUTO)
    
    def autonomousPeriodic(self) -> None:
        self.automanager.run_current_sequence()
        for subsystems in self.subsystems:
            subsystems.update(TorqueMode.AUTO)
        for subsystem in self.subsystems:
            subsystem.clean(TorqueMode.AUTO)
    
    def testInit(self) -> None:
        for subsystem in self.subsystems:
            subsystem.initialize(TorqueMode.TEST)
    
    def testPeriodic(self) -> None:
        self.input.update(TorqueMode.TEST)
        for subsystem in self.subsystems:
            subsystem.update(TorqueMode.TEST)
        for subsystem in self.subsystems:
            subsystem.clean(TorqueMode.TEST)