from classes.file_finder import FileFinder
from pathlib import Path
from typing import List


def test_no_files():
    finder: FileFinder = FileFinder()
    paths: List[Path] = finder.get_file_paths("tests/data/composer", "txt")
    files: List[str] = []
    for path in paths:
        files.append(str(path))
    assert files == []


def test_json_finding():
    finder: FileFinder = FileFinder()
    paths: List[Path] = finder.get_file_paths("tests/data/composer", "json")
    files: List[str] = []
    for path in paths:
        files.append(str(path))
    assert files == ["tests\\data\\composer\\composer.json"]


def test_lock_finding():
    finder: FileFinder = FileFinder()
    paths: List[Path] = finder.get_file_paths("tests/data/composer", "lock")
    files: List[str] = []
    for path in paths:
        files.append(str(path))
    assert files == ["tests\\data\\composer\\composer.lock"]

