import wpilib
from abc import ABC, abstractmethod
from lib.auto.TorqueSequence import TorqueSequence
from lib.auto.TorquePathLoader import TorquePathLoader

class TorqueAutoManager(ABC):
    def __init__(self) -> None:
        self.chooser = wpilib.SendableChooser()
        self.sequences = {}
        self.current_sequence: TorqueSequence | None = None

        self.load_sequences()

        self.path_loader = TorquePathLoader()

        self.display_choices()
    
    def display_choices(self) -> None:
        wpilib.SmartDashboard.putData("Auto List", self.chooser)

    def add_sequence(self, name: str, sequence: TorqueSequence) -> None:
        self.sequences[name] = sequence

        if len(self.sequences) == 0:
            self.chooser.setDefaultOption(name, name)
        else:
            self.chooser.addOption(name, name)
        wpilib.SmartDashboard.putData("Auto List", self.chooser)
    
    def choose_current_sequence(self) -> None:
        self.current_sequence = self.sequences.get(self.chooser.getSelected())
        self.ended = False
    
    def run_current_sequence(self) -> None:
        if self.current_sequence != None:
            self.current_sequence.run()

            self.ended = self.current_sequence.has_ended()

    @abstractmethod
    def load_paths(self) -> None:
        pass
    
    @abstractmethod
    def load_sequences(self) -> None:
        pass