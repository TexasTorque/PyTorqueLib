from wpimath.geometry import Rotation2d
from wpimath import angleModulus

def scaled_linear_deadband(value: float, scale: float) -> float:
    return 0 if abs(value) < scale else (value - (abs(value) / value) * scale) / (1 - scale)

def coterminal(rotation: Rotation2d) -> Rotation2d:
    return Rotation2d(angleModulus(rotation.radians()))