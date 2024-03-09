from __future__ import annotations

class Subsystem:
    def __init__(self, name: str) -> None:
        self.name = name
        self.subsystems: list[Subsystem] = []

    def initialize(self) -> None:
        print(self.name + " has not overridden the initialize function!")

    def update(self) -> None:
        print(self.name + " has not overridden the update function!")
    
    def get_name(self) -> str:
        return self.name
    
    def set_subsystems(self, subsystems: list[Subsystem]) -> None:
        self.subsystems = subsystems

    def get_subsystem(self, name: str) -> Subsystem | None:
        for subsystem in self.subsystems:
            if subsystem.get_name() == name:
                return subsystem