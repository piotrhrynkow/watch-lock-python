from classes.replacer import Replacer
from typing import IO


def test_nonexistent_package():
    text: str = get_lock_fixture("composer.lock")
    replacer: Replacer = Replacer(text)
    assert replacer.find_package("piotrhrynkow/watch-lock") is False


def test_finding_package():
    text: str = get_lock_fixture("composer.lock")
    replacer: Replacer = Replacer(text)
    assert replacer.find_package("doctrine/instantiator") is True
    assert replacer.find_package("phpunit/phpunit") is True
    assert replacer.find_package("webmozart/assert") is True


def test_replace_not_required():
    text: str = get_lock_fixture("composer.lock")
    replacer: Replacer = Replacer(text)
    replacer.find_package("phpunit/phpunit")
    assert replacer.replace_required("34c18baa6a44f1d1fbf0338907139e9dce95b997") is False


def test_replace_required():
    text: str = get_lock_fixture("composer.lock")
    replacer: Replacer = Replacer(text)
    replacer.find_package("phpunit/phpunit")
    assert replacer.replace_required("hashneedsreplace") is True


def test_replace_hashes():
    text: str = get_lock_fixture("composer.lock")
    replacer: Replacer = Replacer(text)
    replacer.find_package("doctrine/instantiator")
    replacer.replace("doctrineinstantiatorhash")
    replacer.find_package("phpunit/phpunit")
    replacer.replace("phpunitphpunithash")
    replacer.find_package("webmozart/assert")
    replaced = replacer.replace("webmozartasserthash")
    assert replaced == get_lock_fixture("only_hashes.lock")


def test_replace_all():
    text: str = get_lock_fixture("composer.lock")
    replacer: Replacer = Replacer(text)
    replacer.find_package("doctrine/instantiator")
    replacer.replace("doctrineinstantiatorhash", "2050-01-01T00:00:01+00:00")
    replacer.find_package("phpunit/phpunit")
    replacer.replace("phpunitphpunithash", "2050-01-02T00:00:02+00:00")
    replacer.find_package("webmozart/assert")
    replaced = replacer.replace("webmozartasserthash", "2050-01-03T00:00:03+00:00")
    assert replaced == get_lock_fixture("replaced_all.lock")


def get_lock_fixture(file_name: str) -> str:
    stream: IO = open("tests/data/composer/" + file_name, "r")
    data = stream.read()
    stream.close()
    return data

