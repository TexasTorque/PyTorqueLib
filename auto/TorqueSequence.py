from lib.auto.TorqueCommand import TorqueCommand

class TorqueSequence:
    def __init__(self) -> None:
        self.commands: list[TorqueCommand] = []
        self.ended = False
        self.index = 0

    def exit(self) -> None:
        self.ended = True
    
    def run(self) -> bool:
        if self.index < len(self.commands):
            command_ended = True
            for command in self.commands:
                if not command.run():
                    command_ended = False
            if command_ended:
                self.index += 1
        elif not self.ended:
            self.ended = True
    
    def has_ended(self) -> bool:
        return self.ended
    
    def reset(self) -> None:
        self.ended = False
        self.block_index = 0
        for block in self.commands:
            for command in block:
                command.reset()
    
    def resetBlock(self) -> None:
        self.ended = False
        for command in self.commands[self.block_index]:
            command.reset()

    def add_command(self, command: TorqueCommand) -> None:
        self.commands.append(command)