"""Input validation functions for CLI prompts."""

from datetime import date, time
from typing import Optional


class ValidationError(Exception):
    """Exception raised when input validation fails."""

    pass


def validate_priority(value: str) -> str:
    """Validate priority input.

    Args:
        value: Priority value to validate.

    Returns:
        Validated priority in lowercase.

    Raises:
        ValidationError: If priority is invalid.
    """
    if not value:
        raise ValidationError("Priority cannot be empty")

    normalized = value.strip().lower()
    valid_priorities = ["high", "medium", "low"]

    if normalized not in valid_priorities:
        raise ValidationError(
            f"Invalid priority '{value}'. Must be one of: high, medium, low"
        )

    return normalized


def validate_category(value: str) -> str:
    """Validate category input.

    Args:
        value: Category value to validate.

    Returns:
        Validated category in lowercase.

    Raises:
        ValidationError: If category is invalid.
    """
    if not value:
        raise ValidationError("Category cannot be empty")

    normalized = value.strip().lower()
    valid_categories = ["work", "home", "uncategorized"]

    if normalized not in valid_categories:
        raise ValidationError(
            f"Invalid category '{value}'. Must be one of: work, home, uncategorized"
        )

    return normalized


def validate_due_date(value: str) -> Optional[date]:
    """Validate due date input.

    Args:
        value: Due date string to validate.

    Returns:
        Validated date object or None if empty.

    Raises:
        ValidationError: If date format is invalid or >10 years future.
    """
    if not value or value.strip() == "":
        return None

    try:
        parsed_date = date.fromisoformat(value.strip())
    except ValueError:
        raise ValidationError(
            f"Invalid date format '{value}'. Expected YYYY-MM-DD (e.g., 2026-01-15)"
        )

    # Check if date is more than 10 years in the future
    today = date.today()
    max_date = date(today.year + 10, today.month, today.day)

    if parsed_date > max_date:
        raise ValidationError(
            f"Date cannot be more than 10 years in the future (max: {max_date.isoformat()})"
        )

    return parsed_date


def validate_due_time(value: str) -> Optional[time]:
    """Validate due time input.

    Args:
        value: Due time string to validate.

    Returns:
        Validated time object or None if empty.

    Raises:
        ValidationError: If time format is invalid.
    """
    if not value or value.strip() == "":
        return None

    try:
        parsed_time = time.fromisoformat(value.strip())
    except ValueError:
        raise ValidationError(
            f"Invalid time format '{value}'. Expected HH:MM in 24-hour format (e.g., 14:30)"
        )

    return parsed_time


def validate_recurrence(value: str) -> Optional[str]:
    """Validate recurrence interval input.

    Args:
        value: Recurrence value to validate.

    Returns:
        Validated recurrence type or None if empty.

    Raises:
        ValidationError: If recurrence type is invalid.
    """
    if not value or value.strip() == "":
        return None

    normalized = value.strip().lower()
    valid_recurrences = ["daily", "weekly", "monthly", "custom"]

    # Check if it's a named recurrence type
    if normalized in valid_recurrences:
        return normalized

    # Check if it's a positive integer (custom interval)
    try:
        interval = int(normalized)
        if interval <= 0:
            raise ValidationError("Custom recurrence interval must be a positive integer")
        return "custom"
    except ValueError:
        raise ValidationError(
            f"Invalid recurrence '{value}'. Must be one of: daily, weekly, monthly, custom, or a positive integer"
        )

    return normalized


def validate_reminder_interval(value: str) -> int:
    """Validate reminder interval input.

    Args:
        value: Reminder interval in minutes.

    Returns:
        Validated positive integer.

    Raises:
        ValidationError: If interval is not a positive integer.
    """
    if not value or value.strip() == "":
        raise ValidationError("Reminder interval cannot be empty")

    try:
        interval = int(value.strip())
        if interval <= 0:
            raise ValidationError("Reminder interval must be a positive integer")
        return interval
    except ValueError:
        raise ValidationError(
            f"Invalid reminder interval '{value}'. Must be a positive integer (minutes)"
        )


def validate_task_id(value: str, task_store) -> int:
    """Validate task ID input.

    Args:
        value: Task ID string to validate.
        task_store: TaskStore to verify task exists.

    Returns:
        Validated task ID.

    Raises:
        ValidationError: If ID is invalid or task doesn't exist.
    """
    if not value or value.strip() == "":
        raise ValidationError("Task ID cannot be empty")

    try:
        task_id = int(value.strip())
        if task_id <= 0:
            raise ValidationError("Task ID must be a positive integer")
    except ValueError:
        raise ValidationError(f"Invalid task ID '{value}'. Must be a positive integer")

    # Verify task exists in store
    task = task_store.get(task_id)
    if task is None:
        raise ValidationError(f"Task with ID {task_id} does not exist")

    return task_id


def validate_title(value: str) -> str:
    """Validate task title.

    Args:
        value: Title to validate.

    Returns:
        Validated title.

    Raises:
        ValidationError: If title is empty or exceeds 255 characters.
    """
    if not value or not value.strip():
        raise ValidationError("Title cannot be empty")

    if len(value) > 255:
        raise ValidationError(f"Title exceeds 255 characters (current: {len(value)})")

    return value.strip()


def validate_description(value: str) -> str:
    """Validate task description.

    Args:
        value: Description to validate.

    Returns:
        Validated description.

    Raises:
        ValidationError: If description exceeds 2000 characters.
    """
    if len(value) > 2000:
        raise ValidationError(
            f"Description exceeds 2000 characters (current: {len(value)})"
        )

    return value.strip()
