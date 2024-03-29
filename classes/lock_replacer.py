import re
from typing import Optional


class LockReplacer:

    def __init__(self, text: str):
        self.text: str = text
        self.part: Optional[str] = None
        self.sha: Optional[str] = None
        self.time: Optional[str] = None

    def find_package(self, package: str) -> bool:
        package = package.replace('/', r'\/')
        regex = r'.+{\s*("name":\s*"' + package + r'",.+?"reference":\s*"([a-z0-9]+)".+?"time":\s*"([0-9T\-:+]+)")'
        matched = re.match(regex, self.text, flags=re.M | re.S)
        if matched is not None:
            self.part, self.sha, self.time = matched.groups()
            return True
        return False

    def replace_required(self, sha: str) -> bool:
        return sha != self.sha

    def replace(self, sha: str, time: str = None) -> str:
        replacement: str = self.part.replace(self.sha, sha)
        if time is not None:
            replacement = replacement.replace(self.time, time)
        self.text = self.text.replace(self.part, replacement)
        return self.text
