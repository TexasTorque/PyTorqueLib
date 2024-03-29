from lib.auto.TorqueCommand import TorqueCommand
from lib.auto.TorqueBlock import TorqueBlock

class TorqueSequence:
    def __init__(self) -> None:
        self.blocks: list[TorqueBlock] = []
        self.ended = False
        self.block_index = 0

    def exit(self) -> None:
        self.ended = True
    
    def run(self) -> bool:
        if self.block_index < len(self.blocks):
            block_ended = True
            for command in self.blocks[self.block_index].get_commands():
                if not command.run():
                    block_ended = False
            if block_ended:
                self.block_index += 1
        elif not self.ended:
            self.ended = True
    
    def has_ended(self) -> bool:
        return self.ended
    
    def reset(self) -> None:
        self.ended = False
        self.block_index = 0
        for block in self.blocks:
            for command in block.get_commands():
                command.reset()
    
    def resetBlock(self) -> None:
        self.ended = False
        for command in self.blocks[self.block_index].get_commands():
            command.reset()

    def add_command(self, command: TorqueCommand) -> None:
        self.blocks.append(command)