import re
from datetime import date


ORDER_PATTERN = re.compile(r"(?:order\s*)?#?\s*([A-Z0-9-]{4,})", re.IGNORECASE)


def extract_order_id(text: str) -> str | None:
    match = ORDER_PATTERN.search(text)
    return match.group(1).upper() if match else None


def days_between(start: str, end: str | None = None) -> int:
    end_date = date.fromisoformat(end) if end else date.today()
    return (end_date - date.fromisoformat(start)).days
