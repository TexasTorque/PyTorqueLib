from lib.auto.TorqueCommand import TorqueCommand
from pathplannerlib.controller import PPRamseteController
from pathplannerlib.path import PathPlannerPath
from pathplannerlib.path import PathPlannerTrajectory
from wpimath.geometry import Pose2d
from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import ChassisSpeeds
from wpilib import DriverStation
import systems, wpilib
from pathplannerlib.telemetry import PPLibTelemetry

class TorqueFollowPath(TorqueCommand):
    def __init__(self) -> None:
        super().__init__()
        
        self.timer = wpilib.Timer()
    
    def init(self) -> None:
        path = PathPlannerPath.fromPathFile('path name') # path supplier

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            path = path.flipPath()
        
        self.trajectory = path.getTrajectory(ChassisSpeeds(), Rotation2d.fromDegrees(systems.drivebase.get_gyro_measurement()))
        
        PPLibTelemetry.setCurrentPath(path)
        
        startingPose = self.trajectory.getInitialDifferentialPose()
        systems.drivebase.set_pose(startingPose)
        self.timer.restart()
        
    def continuous(self) -> None:
        elapsed = self.timer.get()
        desired = self.trajectory.sample(elapsed)
        
        PPLibTelemetry.setCurrentPose(systems.drivebase.get_pose())
        PPLibTelemetry.setTargetPose(desired.getDifferentialPose())
    
    def end_condition(self) -> bool:
        return self.timer.hasElapsed(self.trajectory.getTotalTimeSeconds())
        
    def end(self) -> None:
        self.timer.stop()