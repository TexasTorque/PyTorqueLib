from lib.auto.TorqueCommand import TorqueCommand
import wpilib


class TorqueRunForTime(TorqueCommand):
    def __init__(self, function, time: float) -> None:
        super().__init__()
        
        self.function = function
        self.time = time
        
    def init(self) -> None:
        self.start = wpilib.Timer.getFPGATimestamp()
        
    def continuous(self) -> None:
        self.function()
    
    def end_condition(self) -> bool:
        return wpilib.Timer.getFPGATimestamp() - self.start > self.time
    
    def end(self) -> None:
        pass