from classes.matcher import Matcher
from model.match import Match
from typing import List


def test_json_matches():
    matches: List[Match] = Matcher.get_json_matches("tests/data/config.yaml")
    x_match_names: List[str] = []
    y_match_names: List[str] = []
    x_match_hashes: List[str] = []
    y_match_hashes: List[str] = []
    value_type = ["source", "reference"]
    for match in matches:
        x_match_names.append(match.package_x.name)
        y_match_names.append(match.package_y.name)
        x_match_hashes.append(match.package_x.get_value(value_type))
        y_match_hashes.append(match.package_y.get_value(value_type))
    assert x_match_names == ["phpunit/phpunit"]
    assert y_match_names == ["phpunit/phpunit"]
    assert x_match_hashes == ["34c18baa6a44f1d1fbf0338907139e9dce95b997"]
    assert y_match_hashes == ["34c18baa6a44f1d1fbf0338907139e9dce95b997"]


def test_lock_matches():
    matches: List[Match] = Matcher.get_lock_matches("tests/data/config.yaml")
    x_match_names: List[str] = []
    y_match_names: List[str] = []
    x_match_hashes: List[str] = []
    y_match_hashes: List[str] = []
    value_type = ["source", "reference"]
    for match in matches:
        x_match_names.append(match.package_x.name)
        y_match_names.append(match.package_y.name)
        x_match_hashes.append(match.package_x.get_value(value_type))
        y_match_hashes.append(match.package_y.get_value(value_type))
    assert x_match_names == ["phpunit/php-code-coverage", "phpunit/phpunit"]
    assert y_match_names == ["phpunit/php-code-coverage", "phpunit/phpunit"]
    assert x_match_hashes == ["f1884187926fbb755a9aaf0b3836ad3165b478bf", "34c18baa6a44f1d1fbf0338907139e9dce95b997"]
    assert y_match_hashes == ["f1884187926fbb755a9aaf0b3836ad3165b478bf", "34c18baa6a44f1d1fbf0338907139e9dce95b997"]
