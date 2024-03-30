from abc import ABC, abstractmethod

class TorqueCommand(ABC):
    def __init__(self) -> None:
        self.ended = False
        self.started = False
    
    def run(self) -> bool:
        if self.ended:
            return self.ended
        if not self.started:
            self.init()
            self.started = True
        self.continuous()
        if self.end_condition():
            self.end()
            self.ended = True
        return self.ended
    
    def reset(self) -> None:
        self.end()
        self.ended = False
        self.started = False
    
    def has_ended(self) -> bool:
        return self.ended
    
    @abstractmethod
    def init(self) -> None:
        pass

    @abstractmethod
    def continuous(self) -> None:
        pass

    @abstractmethod
    def end_condition(self) -> bool:
        pass

    @abstractmethod
    def end(self) -> None:
        pass