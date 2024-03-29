from lib.auto.TorqueCommand import TorqueCommand

class TorqueBlock(list):
    def __init__(self, *args: list[TorqueCommand]) -> None:
        for command in args:
            self.append(command)

    def add_command(self, command: TorqueCommand) -> None:
        self.append(command)

    def get_commands(self) -> list[TorqueCommand]:
        return self