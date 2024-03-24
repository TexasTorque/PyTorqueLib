import math
import wpilib
from wpimath.controller import PIDController, SimpleMotorFeedforwardMeters
from phoenix5.sensors import CANCoder
from lib.motor.neo import Neo
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.geometry import Rotation2d

class SwerveModule:
    def __init__(self, name: str, driveID: int, turnID: int, encoderID: int, offset: float) -> None:
        self.name = name
        self.drive = Neo(driveID)
        self.drive.set_current_limit(35)
        self.drive.set_voltage_compensation(12.6)
        self.drive.set_break_mode(True)
        self.drive.set_conversion_factor(.0485823156, 8.097052603e-4)
        self.drive.burn_flash()

        self.turn = Neo(turnID)
        self.turn.set_current_limit(25)
        self.turn.set_voltage_compensation(12.6)
        self.turn.set_break_mode(True)
        self.turn.set_conversion_factor(77.97432966, 1)
        self.turn.burn_flash()

        self.encoder: CANCoder = CANCoder(encoderID)

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
            drivePIDOutput = self.drivePID.calculate(self.drive.get_velocity(), optimized.speed)
            driveFFOutput = self.driveFF.calculate(optimized.speed)

            self.drive.set_percent(drivePIDOutput + driveFFOutput)
        else:
            self.drive.set_percent(optimized.speed / 4.6)

        turnPIDOutput = self.turnPID.calculate(self.get_rotation().radians(), state.angle.radians())
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
        return Rotation2d.fromDegrees((self.encoder.getPosition() - self.offset) * 180 / math.pi)