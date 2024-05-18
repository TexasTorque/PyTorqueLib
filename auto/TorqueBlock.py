from lib.auto.TorqueCommand import TorqueCommand

class TorqueBlock(list[TorqueCommand]):
    def __init__(self, *commands: TorqueCommand) -> None:
        for command in commands:
            self.append(command)

    def add_command(self, command: TorqueCommand) -> None:
        self.append(command)

    def get_commands(self) -> list[TorqueCommand]:
        return self