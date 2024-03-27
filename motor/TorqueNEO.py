import rev

class TorqueNEO:
    def __init__(self, id: int) -> None:
        self.motor = rev.CANSparkMax(id, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.encoder = self.motor.getEncoder()
        self.controller: rev.SparkPIDController = self.motor.getPIDController()
        self.followers: list[rev.CANSparkMax] = []
        self.motor.setInverted(False)
    
    def add_follower(self, id: int, invert: bool) -> None:
        follower = rev.CANSparkMax(id, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.followers.append(follower)
        follower.follow(self.motor, invert)

    def burn_flash(self) -> None:
        self.motor.burnFlash()
    
    def set_break_mode(self, break_: bool) -> None:
        self.motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake if break_ else rev.CANSparkMax.IdleMode.kCoast)
        for follower in self.followers:
            follower.setIdleMode(rev.CANSparkMax.IdleMode.kBrake if break_ else rev.CANSparkMax.IdleMode.kCoast)
    
    def set_percent(self, percent: float) -> None:
        self.motor.set(percent)
    
    def get_controller(self) -> rev.SparkPIDController:
        return self.controller
    
    def set_volts(self, volts: float) -> None:
        self.motor.setVoltage(volts)
    
    def set_voltage_compensation(self, volts: float) -> None:
        self.motor.enableVoltageCompensation(volts)
    
    def disable_voltage_compensation(self) -> None:
        self.motor.disableVoltageCompensation()
    
    def set_current_limit(self, amps: int) -> None:
        self.motor.setSmartCurrentLimit(amps)
    
    def configure_controller(self, p: float, i: float, d: float, ff: float = 0) -> None:
        self.controller.setP(p)
        self.controller.setI(i)
        self.controller.setD(d)
        self.controller.setFF(ff)

    def set_reference(self, goal: float, control: rev.CANSparkMax.ControlType) -> None:
        self.controller.setReference(goal, control)

    def set_conversion_factor(self, posFactor: float, veloFactor: float) -> None:
        self.encoder.setPositionConversionFactor(posFactor)
        self.encoder.setVelocityConversionFactor(veloFactor)

    def set_position(self, pos: float) -> None:
        self.controller.setReference(pos, rev.CANSparkMax.ControlType.kPosition)
    
    def get_position(self) -> float:
        return self.encoder.getPosition()
    
    def set_velocity(self, velocity: float) -> None:
        self.controller.setReference(velocity, rev.CANSparkMax.ControlType.kVelocity)
    
    def get_velocity(self) -> None:
        return self.encoder.getVelocity()
    
    def set_smart_velocity(self, velocity: float) -> None:
        self.controller.setReference(velocity, rev.CANSparkMax.ControlType.kSmartVelocity)
    
    def set_smart_position(self, pos: float) -> None:
        self.controller.setReference(pos, rev.CANSparkMax.ControlType.kSmartMotion)