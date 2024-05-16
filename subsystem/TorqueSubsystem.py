from lib.base.TorqueMode import TorqueMode
from abc import ABC, abstractmethod

class TorqueSubsystem(ABC):
    @abstractmethod
    def initialize(self, mode: TorqueMode) -> None:
        print("Must override the update function!")

    @abstractmethod
    def update(self, mode: TorqueMode) -> None:
        print("Must override the update function!")

    @abstractmethod
    def clean(self, mode: TorqueMode) -> None:
        print("Must override the clean function!")