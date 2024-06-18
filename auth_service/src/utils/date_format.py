from datetime import datetime, timedelta, timezone
from typing import Annotated

from pydantic import Field


def format_datetime_with_timezone(dt: datetime, tz_offset: int) -> str:
    """
    Format datetime with timezone offset
    :param dt: datetime
    :param tz_offset: timezone offset in hours
    :return: formatted datetime
    """
    tz = timezone(timedelta(hours=tz_offset))
    local_dt = dt.astimezone(tz)
    return local_dt.strftime("%Y-%m-%d %H:%M:%S %Z")


class UTCPlus3Datetime(datetime):
    """
    UTC+3 datetime
    """

    def __new__(cls, *args, **kwargs):  # type: ignore
        return datetime.__new__(cls, *args, **kwargs)

    def __str__(self) -> str:
        return format_datetime_with_timezone(self, 3)


utc_plus3 = Annotated[datetime, Field(default_factory=lambda: UTCPlus3Datetime)]
