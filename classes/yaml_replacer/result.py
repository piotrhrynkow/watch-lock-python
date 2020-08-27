from typing import Optional


class Result:

    STATUS_SUCCESS = "success"
    STATUS_IGNORED = "ignored"
    STATUS_FAILED = "failed"

    def __init__(self, package: str):
        self.package: str = package
        self.sha_before: Optional[str] = None
        self.sha_after: Optional[str] = None
        self.status: Optional[str] = None
        self.message: Optional[str] = None

    def set_sha_before(self, sha: str):
        self.sha_before = sha

    def set_sha_after(self, sha: str):
        self.sha_after = sha

    def set_success(self):
        self.status = self.STATUS_SUCCESS

    def set_ignored(self, message: Optional[str] = None):
        self.status = self.STATUS_IGNORED
        self.message = message

    def set_failed(self, message: Optional[str] = None):
        self.status = self.STATUS_FAILED
        self.message = message
