from wpimath.controller import PIDController

class TorquePID:
    def __init__(self, P=1, I=0, D=0) -> None:
        self.P = P
        self.I = I
        self.D = D
        
    def set_p_value(self, P) -> None:
        self.P = P
        
    def set_i_value(self, I) -> None:
        self.I = I
        
    def set_d_value(self, D) -> None:
        self.D = D
        
    def calculate(self) -> PIDController:
        return PIDController(self.P, self.I, self.D)