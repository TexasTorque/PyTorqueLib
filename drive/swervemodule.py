import math
import wpimath.kinematics
import wpimath.geometry
import wpimath.controller
import phoenix6.hardware.cancoder
import motor.neo

kWheelRadius = 0.0508
kEncoderResolution = 4096
kModuleMaxAngularVelocity = math.pi
kModuleMaxAngularAcceleration = math.tau

class SwerveModule:
    def __init__(self, name: str, driveID: int, turnID: int, encoderID: int) -> None:
        self.name = name
        self.drive = motor.neo.Neo(driveID)
        self.drive.set_current_limit(35)
        self.drive.set_voltage_compensation(12.6)
        self.drive.set_break_mode(True)
        # self.drive.set_conversion_factor()
        self.drive.burn_flash()

        self.turn = motor.neo.Neo(turnID)
        self.turn.set_current_limit(25)
        self.turn.set_voltage_compensation(12.6)
        self.turn.set_break_mode(True)
        # self.turn.set_conversion_factor()
        self.turn.burn_flash()

        self.encoder: phoenix6.hardware.cancoder.CANcoder = phoenix6.hardware.cancoder.CANcoder(encoderID)

        self.drivePID = wpimath.controller.PIDController(.1, 0, 0)
        self.turnPID = wpimath.controller.PIDController(.5, 0, 0)
        self.turnPID.enableContinuousInput(-180, 180)
    
    def set_desired_state(self, state: wpimath.kinematics.SwerveModuleState, use_smart_drive: bool) -> None:
        optimized = wpimath.kinematics.SwerveModuleState.optimize(
            state,
            wpimath.geometry.Rotation2d.fromRotations(self.encoder.get_absolute_position().value_as_double
        ))
        