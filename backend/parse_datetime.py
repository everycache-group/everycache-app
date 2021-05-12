from datetime import date, datetime


class DateParseError(Exception):
    """Raised when date parsing fails"""


class DateTimeParseError(Exception):
    """Raised when datetime parsing fails"""


def parse_date(date_str: str) -> date:
    try:
        return date.fromisoformat(date_str)
    except ValueError as e:
        raise DateParseError(
            f"{e}. Please use the proper format: 'YYYY-mm-dd', for example: 2021-05-09"
        )


def parse_datetime(datetime_str: str) -> date:
    try:
        return datetime.fromisoformat(datetime_str)
    except ValueError as e:
        raise DateTimeParseError(
            f"{e}. Please use the proper format, 'YYYY-mm-ddTHH:MM for example: "
            "2021-05-09T13:25"
        )
