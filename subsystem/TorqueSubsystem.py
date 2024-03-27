from lib.base.TorqueMode import TorqueMode

class TorqueSubsystem:
    def initialize(self, mode: TorqueMode) -> None:
        print("Must override the update function!")

    def update(self, mode: TorqueMode) -> None:
        print("Must override the update function!")