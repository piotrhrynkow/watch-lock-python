from typing import Optional


class Result:

    STATUS_SUCCESS = "success"
    STATUS_IGNORED = "ignored"
    STATUS_WARNING = "warning"
    STATUS_FAILED = "failed"

    def __init__(self):
        self.status: Optional[str] = None
        self.directory: Optional[str] = None
        self.message: Optional[str] = None

    def is_success(self) -> bool:
        return self.STATUS_SUCCESS == self.status

    def is_failed(self) -> bool:
        return self.STATUS_FAILED == self.status

    def set_success(self):
        self.status = self.STATUS_SUCCESS

    def set_ignored(self, message: Optional[str] = None):
        self.status = self.STATUS_IGNORED
        self.message = message

    def set_warning(self, message: Optional[str] = None):
        self.status = self.STATUS_WARNING
        self.message = message

    def set_failed(self, message: Optional[str] = None):
        self.status = self.STATUS_FAILED
        self.message = message