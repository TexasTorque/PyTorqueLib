from __future__ import annotations
import rev

class TorqueNEO:
    def __init__(self, id: int) -> None:
        self.motor = rev.SparkMax(id, rev.SparkLowLevel.MotorType.kBrushless)
        self.config = rev.SparkMaxConfig()
    
    def invert(self, invert: bool) -> TorqueNEO:
        self.config.inverted(invert)
        return self
    
    def idle_mode(self, idle_mode: rev.SparkMaxConfig.IdleMode) -> TorqueNEO:
        self.config.setIdleMode(idle_mode)
        return self
    
    def pid(self, p: float, i: float, d: float) -> TorqueNEO:
        self.config.closedLoop.pid(p, i, d)
        return self
    
    def pidf(self, p: float, i: float, d: float, f: float) -> TorqueNEO:
        self.config.closedLoop.pidf(p, i, d, f)
        return self
    
    def voltage_compensation(self, voltage: float) -> TorqueNEO:
        self.config.voltageCompensation(voltage)
        return self
    
    def disable_voltage_compensation(self) -> TorqueNEO:
        self.config.disableVoltageCompensation()
        return self
    
    def current_limit(self, limit: int) -> TorqueNEO:
        self.config.smartCurrentLimit(limit)
        return self
    
    def conversion_factors(self, pos_factor: float, velo_factor: float) -> TorqueNEO:
        self.config.encoder.positionConversionFactor(pos_factor)
        self.config.encoder.velocityConversionFactor(velo_factor)
        return self
    
    def apply(self) -> TorqueNEO:
        self.motor.configure(self.config, rev.SparkBase.ResetMode.kResetSafeParameters, rev.SparkBase.PersistMode.kPersistParameters)
        return self
    
    def set_percent(self, percent: float) -> None:
        self.motor.set(percent)

    def get_percent(self) -> float:
        return self.motor.get()
    
    def set_volts(self, volts: float) -> None:
        self.motor.setVoltage(volts)

    def get_volts(self) -> float:
        return self.motor.getAppliedOutput()
    
    def get_bus_voltage(self) -> float:
        return self.motor.getBusVoltage()
    
    def get_output_current(self) -> float:
        return self.motor.getOutputCurrent()
    
    def get_position(self) -> float:
        return self.motor.getEncoder().getPosition()

    def get_velocity(self) -> float:
        return self.motor.getEncoder().getVelocity()
