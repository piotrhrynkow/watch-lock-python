import glob
from pathlib import Path
from typing import List


class FileFinder:

    @staticmethod
    def get_file_paths(directory: str, extension: str) -> List[Path]:
        lock_files = []
        lock_paths = glob.glob(directory + "/composer." + extension, recursive=True)
        for file in lock_paths:
            lock_files.append(Path(file))
        return lock_files

    @staticmethod
    def get_lock_path(json_path) -> Path:
        return json_path.joinpath(json_path.parent, "composer.lock")
