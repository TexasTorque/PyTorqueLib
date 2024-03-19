import wpilib
import systems

class TorqueRobotBase(wpilib.TimedRobot):

    def __init__(self) -> None:
        super().__init__()
        systems.add_subsystems()
    
    def robotInit(self) -> None:
        systems.init_subsystems()
    
    def teleopPeriodic(self) -> None:
        systems.update_subsystems()
    
    def disabledPeriodic(self) -> None:
        pass

    def robotPeriodic(self) -> None:
        pass

    def _simulationPeriodic(self) -> None:
        pass