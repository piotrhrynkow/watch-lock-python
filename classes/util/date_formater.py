from datetime import datetime, timezone


class DateFormater:

    COMPOSER_FORMAT = "%Y-%m-%dT%H:%M:%S+00:00"

    @staticmethod
    def get_current_utc_datetime(format: str = COMPOSER_FORMAT):
        return datetime.now(timezone.utc).strftime(format)
