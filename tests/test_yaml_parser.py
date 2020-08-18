from classes.yaml_parser import YamlParser
import pytest


def test_file_not_found():
    yaml = YamlParser("tests/data/missing.yaml")
    with pytest.raises(Exception):
        yaml.get_directories()


def test_path_is_not_file():
    yaml = YamlParser("tests/data")
    with pytest.raises(Exception):
        yaml.get_directories()


def test_should_return_directories():
    yaml = YamlParser("tests/data/config.yaml")
    directories = yaml.get_directories()
    assert directories == ['./*']


def test_should_return_packages():
    yaml = YamlParser("tests/data/config.yaml")
    packages = yaml.get_packages()
    package_names = []
    for package in packages:
        package_names.append(package.name)
    assert package_names == ['phpunit/phpunit']

