import wpilib
from lib.subsystem.TorqueSubsystem import TorqueSubsystem
from lib.base.TorqueMode import TorqueMode
from auto.automanager import AutoManager

class TorqueRobotBase(wpilib.TimedRobot):
    def __init__(self) -> None:
        super().__init__()
        self.subsystems: list[TorqueSubsystem] = []
        self.input: TorqueSubsystem | None = None
        self.lights: TorqueSubsystem | None = None
        self.perception: TorqueSubsystem | None = None
        self.auto_manager: AutoManager | None = None
    
    def set_input(self, input: TorqueSubsystem) -> None:
        self.input = input
    
    def set_lights(self, lights: TorqueSubsystem) -> None:
        self.lights = lights

    def set_perception(self, perception: TorqueSubsystem) -> None:
        self.perception = perception
    
    def set_auto_manager(self, auto_manager: AutoManager) -> None:
        self.auto_manager = auto_manager
    
    def add_subsystem(self, subsystem: TorqueSubsystem) -> None:
        self.subsystems.append(subsystem)
    
    def disabledPeriodic(self) -> None:
        wpilib.SmartDashboard.updateValues()

    def robotInit(self) -> None:
        if self.auto_manager != None:
            self.auto_manager.load_paths()
        if self.lights != None:
            self.lights.initialize(TorqueMode.ROBOT)
        if self.perception != None:
            self.perception.initialize(TorqueMode.ROBOT)

    def robotPeriodic(self) -> None:
        if self.lights != None:
            self.lights.update(TorqueMode.ROBOT)
        if self.perception != None:
            self.perception.update(TorqueMode.ROBOT)
    
    def teleopInit(self) -> None:
        if self.input != None:
            self.input.initialize(TorqueMode.TELEOP)
        for subsystem in self.subsystems:
            subsystem.initialize(TorqueMode.TELEOP)
    
    def teleopPeriodic(self) -> None:
        if self.input != None:
            self.input.update(TorqueMode.TELEOP)
        for subsystem in self.subsystems:
            subsystem.update(TorqueMode.TELEOP)
        for subsystem in self.subsystems:
            subsystem.clean(TorqueMode.TELEOP)

    def autonomousInit(self) -> None:
        if self.auto_manager != None:
            self.auto_manager.choose_current_sequence()
        if self.input != None:
            self.input.initialize(TorqueMode.AUTO)
        for subsystem in self.subsystems:
            subsystem.initialize(TorqueMode.AUTO)
    
    def autonomousPeriodic(self) -> None:
        if self.input != None:
            self.input.update(TorqueMode.AUTO)
        if self.auto_manager != None:
            self.auto_manager.run_current_sequence()
        for subsystems in self.subsystems:
            subsystems.update(TorqueMode.AUTO)
        for subsystem in self.subsystems:
            subsystem.clean(TorqueMode.AUTO)
    
    def testInit(self) -> None:
        if self.input != None:
            self.input.initialize(TorqueMode.TEST)
        for subsystem in self.subsystems:
            subsystem.initialize(TorqueMode.TEST)
    
    def testPeriodic(self) -> None:
        if self.input != None:
            self.input.update(TorqueMode.TEST)
        for subsystem in self.subsystems:
            subsystem.update(TorqueMode.TEST)
        for subsystem in self.subsystems:
            subsystem.clean(TorqueMode.TEST)