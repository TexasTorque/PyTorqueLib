class Subsystem:
    def __init__(self, name: str) -> None:
        self.name = name

    def initialize(self) -> None:
        print(self.name + " has not overridden the initialize function!")

    def update(self) -> None:
        print(self.name + " has not overridden the update function!")
    
    def get_name(self) -> str:
        return self.name