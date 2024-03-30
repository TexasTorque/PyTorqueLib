from lib.auto.TorqueCommand import TorqueCommand
from pathplannerlib.controller import PPRamseteController
from pathplannerlib.path import PathPlannerPath
from pathplannerlib.path import PathPlannerTrajectory
from wpimath.geometry import Pose2d
from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import ChassisSpeeds
from wpilib import DriverStation
from wpilib import Timer
from subsystems.Drivebase import Drivebase, get_drivebase
from pathplannerlib.telemetry import PPLibTelemetry

class TorqueFollowPath(TorqueCommand):
    def __init__(self) -> None:
        super().__init__()
        
        self.drivebase = get_drivebase()
        
        self.timer = Timer()
        
        self.prevTranslation = Translation2d()
        
        PathPlannerPath.fromPathFile('path name') # set path name here

        path = PathPlannerPath() #fix later
        
        trajectory = PathPlannerTrajectory
        
        self.trajectory = path.getTrajectory(ChassisSpeeds(), Rotation2d.fromDegrees(self.drivebase.get_gyro_measurement()))
        endPosition = self.trajectory.getEndState().getDifferentialPose()
        
        PPLibTelemetry.setCurrentPath(path)
        
        startingPose = self.trajectory.getInitialDifferentialPose()
        self.drivebase.setPose(startingPose)
        self.timer.restart()
        
        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            path = path.flipPath()
        
    def continuous(self) -> None:
        
        elapsed = self.timer.get()
        desired = self.trajectory.sample(elapsed)
        
        PPLibTelemetry.setCurrentPose(self.drivebase.getPose())
        PPLibTelemetry.setTargetPose(desired.getDifferentialPose())
        
    def end(self) -> None:
        self.timer.stop()