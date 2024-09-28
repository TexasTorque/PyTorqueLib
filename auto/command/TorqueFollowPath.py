from lib.auto.TorqueCommand import TorqueCommand
from pathplannerlib.controller import PPHolonomicDriveController
from pathplannerlib.path import PathPlannerPath
from pathplannerlib.path import PathPlannerTrajectory
from pathplannerlib.controller import PIDConstants
from wpimath.geometry import Pose2d
from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import ChassisSpeeds
from wpilib import DriverStation
import systems, wpilib, math
from pathplannerlib.telemetry import PPLibTelemetry

class TorqueFollowPath(TorqueCommand):
    def __init__(self, path_name: str) -> None:
        super().__init__()
        
        self.path_name = path_name
        self.timer = wpilib.Timer()

        self.controller = PPHolonomicDriveController(PIDConstants(10, 0, 0), PIDConstants(math.pi, 0, 0), 4.6, systems.drivebase.get_radius())
    
    def init(self) -> None:
        print("init follow path")
        self.path = PathPlannerPath.fromPathFile(self.path_name)

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            self.path = self.path.flipPath()
        
        self.trajectory = self.path.getTrajectory(ChassisSpeeds(), Rotation2d.fromDegrees(systems.drivebase.get_gyro_measurement()))
        
        PPLibTelemetry.setCurrentPath(self.path)
        
        startingPose = self.trajectory.getInitialDifferentialPose()
        systems.drivebase.pose = startingPose
        self.timer.restart()
        
    def continuous(self) -> None:
        elapsed = self.timer.get()
        desired = self.trajectory.sample(elapsed)

        speeds = self.controller.calculateRobotRelativeSpeeds(systems.drivebase.get_pose(), desired)

        systems.drivebase.set_speeds(speeds.vx, speeds.vy, speeds.omega)
        
        PPLibTelemetry.setCurrentPose(systems.drivebase.get_pose())
        PPLibTelemetry.setTargetPose(desired.getDifferentialPose())
    
    def end_condition(self) -> bool:
        return self.timer.hasElapsed(self.trajectory.getTotalTimeSeconds())
        
    def end(self) -> None:
        self.timer.stop()
        systems.drivebase.set_speeds(0, 0, 0)