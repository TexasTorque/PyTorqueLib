from navx import AHRS
from wpilib import SPI
from wpimath.geometry import Rotation2d

class TorqueNavXGyro(AHRS):
    def __init__(self) -> None:
        super().__init__(SPI.Port.kMXP)
        self.offset = 0
        self.getFusedHeading()

    def calculate_offset_cw(self, offset: float) -> float:
        return (offset - self.getFusedHeading()) % 360
    
    def set_offset_ccw(self, offset: float) -> None:
        self.offset = 360 - self.calculate_offset_cw(offset)

    def get_degrees_cw(self) -> float:
        return (self.getFusedHeading() + self.offset) % 360

    def get_degrees_ccw(self) -> float:
        return 360 - self.get_degrees_cw()
    
    def get_heading_ccw(self) -> Rotation2d:
        return Rotation2d.fromDegrees(self.get_degrees_ccw())
    
    def get_heading_cw(self) -> Rotation2d:
        return Rotation2d.fromDegrees(self.get_degrees_cw())