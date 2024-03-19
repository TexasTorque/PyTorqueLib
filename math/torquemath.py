def scaled_linear_deadband(value: float, scale: float) -> float:
    return 0 if abs(value) < scale else (value - (abs(value) / value) * scale) / (1 - scale)