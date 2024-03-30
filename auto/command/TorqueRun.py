from lib.auto.TorqueCommand import TorqueCommand

class TorqueRun(TorqueCommand):
    def __init__(self, function) -> None:
        self.function = function

    def init(self) -> None:
        self.function()
    
    def continuous(self) -> None:
        pass

    def end_condition(self) -> bool:
        return True
    
    def end(self) -> None:
        pass