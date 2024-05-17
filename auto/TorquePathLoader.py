from pathplannerlib.auto import PathPlannerPath

class TorquePathLoader:
    def __init__(self) -> None:
        self.trajectories: dict[str, PathPlannerPath] = {}

    def preload_path(self, path_name: str) -> None:
        if self.trajectories.get(path_name):
            return
        self.trajectories[path_name] = PathPlannerPath.fromPathFile(path_name)