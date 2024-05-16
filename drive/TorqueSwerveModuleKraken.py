import math
import wpilib
from wpimath.controller import PIDController, SimpleMotorFeedforwardMeters
from phoenix5.sensors import CANCoder
from lib.motor.TorqueNEO import TorqueNEO
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.geometry import Rotation2d
from lib.util.TorqueMath import coterminal
from phoenix6.hardware import TalonFX
from phoenix6.configs import TalonFXConfiguration
from phoenix6.signals import InvertedValue
from phoenix6.signals import NeutralModeValue
from phoenix6.controls import DutyCycleOut

class SwervePorts:
    def __init__(self, driveID, turnID, encoderID) -> None:
        self.driveID = driveID
        self.turnID = turnID
        self.encoderID = encoderID

class TorqueSwerveModuleKraken:
    def __init__(self, name: str, ports: SwervePorts, offset: float = 0) -> None:
        self.name = name

        self.drive_config = TalonFXConfiguration()

        self.drive_config.motor_output.inverted = InvertedValue.CLOCKWISE_POSITIVE
        self.drive_config.motor_output.neutral_mode = NeutralModeValue.BRAKE
        self.drive_config.feedback.sensor_to_mechanism_ratio = 6.75
        self.drive_config.feedback.rotor_to_sensor_ratio = 1
        self.drive_config.current_limits.supply_current_limit_enable = True
        self.drive_config.current_limits.supply_current_limit = 35
        self.drive_config.current_limits.supply_current_threshold = 60
        self.drive_config.current_limits.supply_time_threshold = 0.1
        self.drive_config.current_limits.stator_current_limit_enable = True
        self.drive_config.current_limits.stator_current_limit = 50
        self.drive_config.open_loop_ramps.duty_cycle_open_loop_ramp_period = 0
        self.drive_config.open_loop_ramps.voltage_open_loop_ramp_period = 0
        self.drive_config.closed_loop_ramps.duty_cycle_closed_loop_ramp_period = 0
        self.drive_config.closed_loop_ramps.voltage_closed_loop_ramp_period = 0

        self.drive = TalonFX(ports.driveID)
        self.drive.configurator.apply(self.drive_config)
        self.drive.configurator.set_position(0)

        self.drive_duty_cycle = DutyCycleOut(0)

        self.turn = TorqueNEO(ports.turnID)
        self.turn.set_current_limit(25)
        self.turn.set_voltage_compensation(12.6)
        self.turn.set_break_mode(True)
        self.turn.set_conversion_factor(77.97432966, 1)
        self.turn.burn_flash()

        self.encoder: CANCoder = CANCoder(ports.encoderID)

        self.offset = offset

        self.drivePID = PIDController(.1, 0, 0)
        self.turnPID = PIDController(.5, 0, 0)
        self.turnPID.enableContinuousInput(-math.pi, math.pi)
        self.driveFF = SimpleMotorFeedforwardMeters(.1, .2)

        self.aggregate_position = SwerveModulePosition(0, Rotation2d.fromDegrees(0))
        self.last_sampled_time = -1
    
    def set_desired_state(self, state: SwerveModuleState, use_smart_drive: bool = False) -> None:
        optimized = SwerveModuleState.optimize(state, self.get_rotation())
        
        if use_smart_drive:
            drivePIDOutput = self.drivePID.calculate(self.drive.get_velocity().value_as_double, optimized.speed)
            driveFFOutput = self.driveFF.calculate(optimized.speed)

            self.drive_duty_cycle.output = drivePIDOutput + driveFFOutput
        else:
            self.drive_duty_cycle.output = optimized.speed / 4.6

        turnPIDOutput = self.turnPID.calculate(self.get_rotation().radians(), state.angle.radians())
        self.turn.set_percent(turnPIDOutput)

        self.drive.set_control(self.drive_duty_cycle)

        if not wpilib.RobotBase.isReal():
            time = wpilib.Timer.getFPGATimestamp()
            if self.last_sampled_time == -1:
                self.last_sampled_time = time
            delta_time = time - self.last_sampled_time
            self.last_sampled_time = time
            self.aggregate_position.distance += optimized.speed * delta_time
            self.aggregate_position.angle = optimized.angle
    
    def get_state(self) -> SwerveModuleState:
        return SwerveModuleState(self.drive.get_velocity().value_as_double, self.get_rotation())
    
    def get_position(self) -> SwerveModulePosition:
        if not wpilib.RobotBase.isReal():
            return self.aggregate_position
        return SwerveModulePosition(self.drive.get_position().value_as_double, self.get_rotation())
    
    def get_rotation(self) -> Rotation2d:
        return coterminal(Rotation2d.fromDegrees((self.encoder.getPosition() - self.offset) * 180 / math.pi))