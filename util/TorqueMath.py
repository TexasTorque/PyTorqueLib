from wpimath.geometry import Rotation2d
from wpimath import angleModulus
import numpy as np
import math

class TorquePolynomialRegression:
    def __init__(self, x: list[float | int], y: list[float | int]) -> None:
        self.model = np.polyfit(x, y, 2)
        self.inference = np.poly1d(self.model)

    def predict(self, x: float | int):
        return self.inference(x)

def clamp(n: float, limit: float, negative: bool = True):
    if negative:
        if n > limit or n < -limit: return math.copysign(limit, n) 
        else: return n
    else:
        if n > limit: return limit
        if n < 0: return 0
        else: return n

def scaled_linear_deadband(value: float, scale: float) -> float:
    return 0 if abs(value) < scale else (value - (abs(value) / value) * scale) / (1 - scale)

def coterminal(rotation: Rotation2d) -> Rotation2d:
    return Rotation2d(angleModulus(rotation.radians()))

def constrain(n: float, a: float) -> float:
    return max(min(n, a), -a)

def tolerenced(num: float, target: float, by: float) -> bool:
    return num > target - by and num < target + by