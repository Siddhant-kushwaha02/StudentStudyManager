"""Small input-validation helpers shared by the GUI and backend modules."""

from datetime import datetime


def require_text(value, field_name):
    """Return stripped text or raise a useful validation error."""
    cleaned_value = value.strip()
    if not cleaned_value:
        raise ValueError(f"{field_name} cannot be empty.")
    return cleaned_value


def normalize_due_date(value):
    """Accept YYYY-MM-DD or DD-MM-YYYY and return YYYY-MM-DD."""
    cleaned_value = require_text(value, "Due date")
    for date_format in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(cleaned_value, date_format).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError("Enter a valid date as YYYY-MM-DD or DD-MM-YYYY.")


def validate_priority(value):
    """Return a consistently-cased supported priority."""
    priority = require_text(value, "Priority").title()
    if priority not in {"Low", "Medium", "High"}:
        raise ValueError("Priority must be Low, Medium, or High.")
    return priority
