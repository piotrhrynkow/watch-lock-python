from classes.date_formater import DateFormater
from classes.lock_modifier.result import Result
from classes.lock_replacer import LockReplacer
from classes.yaml_parser import YamlParser
from model.match import Match
from pathlib import Path
from typing import IO, List, Optional


class LockModifier:

    def __init__(self, config_path: str):
        self.yaml_parser = YamlParser(config_path)

    def update_package(self, match: Match, fiels: List[str]) -> Result:
        lock_path: Path = match.lock_path
        package: str = match.package_x.name
        sha: str = match.package_x.get_value(fiels)
        result: Result = Result(package)
        stream: Optional[IO] = None
        try:
            stream, data = self.__get_stream_with_data(lock_path)
            time: str = DateFormater.get_current_utc_datetime()
            replacer: LockReplacer = LockReplacer(data)
            if replacer.find_package(package):
                result.directory = lock_path.resolve().parent
                if not replacer.replace_required(sha):
                    result.set_ignored("Current sha, no required action")
                else:
                    lock_content: str = replacer.replace(sha, time)
                    length: int = self.__save_content(stream, lock_content)
                    if length == len(lock_content):
                        result.set_success()
                    else:
                        result.set_warning("Saved {expected} characters instead of {actual}".format(
                            expected=len(lock_content), actual=length
                        ))
        except Exception as exception:
            result.set_failed(self.__get_exception_message(exception))
        self.__close_stream(stream)
        return result

    def __save_content(self, stream: IO, content: str) -> int:
        stream.seek(0)
        length = stream.write(content)
        stream.truncate()
        return length

    def __get_stream_with_data(self, path: Path) -> List:
        stream = path.open("r+")
        data = stream.read()
        return [stream, data]

    def __close_stream(self, stream: Optional[IO]):
        if isinstance(stream, IO) and not stream.closed:
            stream.close()

    def __get_exception_message(self, exception: Exception) -> Optional[str]:
        return exception.message if hasattr(exception, 'message') else None
