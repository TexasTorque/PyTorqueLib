from __future__ import annotations
import math
import wpilib
from wpimath.controller import PIDController, SimpleMotorFeedforwardMeters
from phoenix6.hardware import CANcoder
from lib.motor.TorqueNEO import TorqueNEO
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.geometry import Rotation2d
from lib.util.TorqueMath import coterminal
from ports import SwervePorts

# Works on Fuse with custom swerve modules

class SwerveConfig:
    def __init__(self, free_wheel_speed: float = 4.6, drive_gear_ratio: float = 6.75, turn_gear_ratio: float = 13.71,
                 drive_p: float = .1, drive_i: float = 0, drive_d: float = 0, drive_ff: float = .2, drive_max_current: int = 35,
                 turn_p: float = .5, turn_i: float = 0, turn_d: float = 0, turn_max_current: int = 25,
                 voltage_compensation: float = 12.6, max_acceleration: float = 3, max_angular_velocity: float = math.pi,
                 max_angular_acceleration: float = math.pi, wheel_diameter: float = 4 * .0254
                 ) -> None:
        self.free_wheel_speed = free_wheel_speed
        self.max_velocity = free_wheel_speed
        self.drive_gear_ratio = drive_gear_ratio
        self.turn_gear_ratio = turn_gear_ratio
        self.drive_p = drive_p
        self.drive_i = drive_i
        self.drive_d = drive_d
        self.drive_ff = drive_ff
        self.drive_max_current = drive_max_current
        self.turn_max_current = turn_max_current
        self.turn_p = turn_p
        self.turn_i = turn_i
        self.turn_d = turn_d
        self.voltage_compensation = voltage_compensation
        self.max_acceleration = max_acceleration
        self.max_angular_velocity = max_angular_velocity
        self.max_angular_acceleration = max_angular_acceleration
        self.wheel_diameter = wheel_diameter

        self.drive_velocity_factor = (1 / drive_gear_ratio / 60) * (wheel_diameter * math.pi)
        self.drive_pose_factor = (1 / drive_gear_ratio) * (wheel_diameter * math.pi) 

class TorqueSwerveModule2022:
    def __init__(self, name: str, ports: SwervePorts, offset: float = 0, config: SwerveConfig = SwerveConfig()) -> None:
        self.name = name
        self.config = config

        self.drive = TorqueNEO(ports.driveID)
        self.drive.set_current_limit(config.drive_max_current)
        self.drive.set_voltage_compensation(config.voltage_compensation)
        self.drive.set_break_mode(True)
        self.drive.set_conversion_factor(config.drive_pose_factor, config.drive_velocity_factor)
        self.drive.burn_flash()

        self.turn = TorqueNEO(ports.turnID)
        self.turn.set_current_limit(config.turn_max_current)
        self.turn.set_voltage_compensation(config.voltage_compensation)
        self.turn.set_break_mode(True)
        self.turn.set_conversion_factor(config.turn_gear_ratio * 2 * math.pi, 1)
        self.turn.burn_flash()

        self.encoder = CANcoder(ports.encoderID)

        self.offset = offset

        self.drivePID = PIDController(config.drive_p, config.drive_i, config.drive_d)
        self.turnPID = PIDController(config.turn_p, config.turn_i, config.turn_d)
        self.turnPID.enableContinuousInput(-math.pi, math.pi)
        self.driveFF = SimpleMotorFeedforwardMeters(config.drive_p, config.drive_ff)

        self.drive_reversed = False
        self.turn_reversed = False
        self.disabled = False

        self.aggregate_position = SwerveModulePosition(0, Rotation2d.fromDegrees(0))
        self.last_sampled_time = -1
    
    def set_desired_state(self, state: SwerveModuleState, use_smart_drive: bool = False) -> None:
        optimized = SwerveModuleState.optimize(state, self.get_rotation())
        
        if use_smart_drive:
            drivePIDOutput = self.drivePID.calculate(self.drive.get_velocity(), optimized.speed)
            driveFFOutput = self.driveFF.calculate(optimized.speed)

            self.drive.set_percent(drivePIDOutput + driveFFOutput)
        else:

            if self.drive_reversed:
                self.drive.set_percent(-optimized.speed / self.config.max_velocity)
            else:
                self.drive.set_percent(optimized.speed / self.config.max_velocity)

        turnPIDOutput = -self.turnPID.calculate(self.get_rotation().radians(), optimized.angle.radians())

        if self.turn_reversed:
            turnPIDOutput = -turnPIDOutput

        if not self.disabled:
            self.turn.set_percent(turnPIDOutput)

        if not wpilib.RobotBase.isReal():
            time = wpilib.Timer.getFPGATimestamp()
            if self.last_sampled_time == -1:
                self.last_sampled_time = time
            delta_time = time - self.last_sampled_time
            self.last_sampled_time = time
            self.aggregate_position.distance += optimized.speed * delta_time
            self.aggregate_position.angle = optimized.angle
    
    def get_state(self) -> SwerveModuleState:
        return SwerveModuleState(self.drive.get_velocity(), self.get_rotation())
    
    def get_position(self) -> SwerveModulePosition:
        if not wpilib.RobotBase.isReal():
            return self.aggregate_position
        return SwerveModulePosition(self.drive.get_position(), self.get_rotation())
    
    def get_rotation(self) -> Rotation2d:
        return coterminal(Rotation2d((self.encoder.get_absolute_position().value_as_double) * 2 * math.pi))
    
    def disable(self, disabled: bool = True) -> TorqueSwerveModule2022:
        self.disabled = disabled
        return self
    
    def reverse_drive(self, reverse: bool = True) -> TorqueSwerveModule2022:
        self.drive_reversed = reverse
        return self
    
    def reverse_turn(self, reverse: bool = True) -> TorqueSwerveModule2022:
        self.turn_reversed = reverse
        return self