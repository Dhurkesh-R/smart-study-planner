import datetime
import random
import string
from typing import Union

def generate_random_id(length: int = 8) -> str:
    """Generates a random alphanumeric ID of given length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def iso_datetime_now(offset_minutes: int = 0) -> str:
    """Returns current time in ISO 8601 format, with optional offset in minutes."""
    now = datetime.datetime.utcnow() + datetime.timedelta(minutes=offset_minutes)
    return now.isoformat()

def validate_input_keys(data: dict, required_keys: list) -> Union[None, str]:
    """Checks if required keys exist in input data; returns missing key or None."""
    for key in required_keys:
        if key not in data:
            return key
    return None

def minutes_from_hours(hours: float) -> int:
    """Converts fractional hours to integer minutes."""
    return int(hours * 60)

def format_study_session(subject: str, interval_minutes: int) -> str:
    """Creates a human-readable summary for a scheduled session."""
    return f"Study session for '{subject}' scheduled in {interval_minutes} days."

def to_title_case(text: str) -> str:
    """Converts a string to title case (for subject names, etc)."""
    return text.strip().title()
