"""Display formatting functions for CLI output."""

from datetime import date, time, datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.task import Task
    from src.models.recurrence import RecurrencePattern


def format_due_datetime(due_date: Optional[date], due_time: Optional[time]) -> str:
    """Format due date and time for display.

    Args:
        due_date: Due date or None.
        due_time: Due time or None.

    Returns:
        Formatted string like "2026-01-10 17:00" or "2026-01-10" or "-".
    """
    if due_date is None:
        return "-"

    if due_time is None:
        return due_date.isoformat()

    return f"{due_date} {due_time}"


def format_overdue_indicator(task: "Task") -> str:
    """Get overdue indicator for task.

    Args:
        task: Task to check.

    Returns:
        "[OVERDUE]" if task is overdue, empty string otherwise.
    """
    # Import here to avoid circular import
    from src.models.task import TaskStatus
    if task.status == TaskStatus.COMPLETE:
        return ""

    due_dt = task.get_full_due_datetime()
    if due_dt is None:
        return ""

    if datetime.now() > due_dt:
        return "[OVERDUE]"

    return ""


def format_recurrence(recurrence: Optional["RecurrencePattern"]) -> str:
    """Format recurrence pattern for display.

    Args:
        recurrence: Recurrence pattern or None.

    Returns:
        Formatted string like "Daily", "Weekly", "3d", or "-".
    """
    if recurrence is None:
        return "-"

    if recurrence.interval_type == recurrence.interval_type.DAILY:
        return "Daily"
    elif recurrence.interval_type == recurrence.interval_type.WEEKLY:
        return "Weekly"
    elif recurrence.interval_type == recurrence.interval_type.MONTHLY:
        return "Monthly"
    elif recurrence.interval_type == recurrence.interval_type.CUSTOM:
        return f"{recurrence.interval_value}d"

    return "-"


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max_length and add ellipsis if truncated.

    Args:
        text: Text to truncate.
        max_length: Maximum length of text.

    Returns:
        Truncated text with ellipsis if needed.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_task_row(task: "Task") -> str:
    """Format a single task for table display.

    Args:
        task: Task to format.

    Returns:
        Formatted string for table row.
    """
    from src.models.task import TaskStatus

    status_marker = "[X]" if task.status == TaskStatus.COMPLETE else "[ ]"
    overdue_indicator = format_overdue_indicator(task)
    title_with_indicator = f"{overdue_indicator} {task.title}" if overdue_indicator else task.title
    # Truncate long titles
    title_with_indicator = truncate_text(title_with_indicator, 50)
    due_str = format_due_datetime(task.due_date, task.due_time)
    recurrence_str = format_recurrence(task.recurrence)

    # Calculate column widths based on content
    id_width = len(str(task.id)) + 2
    status_width = 6
    priority_width = len(task.priority.value) + 2
    category_width = len(task.category.value) + 2
    due_width = max(len(due_str), 12)
    recurrence_width = max(len(recurrence_str), 8)

    return (
        f"{task.id:<{id_width}}│ {status_marker:<{status_width}}│ {task.priority.value:<{priority_width}}│ "
        f"{task.category.value:<{category_width}}│ {due_str:<{due_width}}│ {recurrence_str:<{recurrence_width}}│ {title_with_indicator}"
    )


import shutil


def get_terminal_width() -> int:
    """Get the current terminal width.

    Returns:
        Width of the terminal in characters, defaulting to 80 if unable to determine.
    """
    try:
        width = shutil.get_terminal_size().columns
        return max(width, 80)  # Minimum width of 80
    except Exception:
        return 80  # Default to 80 if unable to get terminal size


def format_table_header(tasks: List["Task"]) -> str:
    """Format the table header for task display.

    Args:
        tasks: List of tasks to determine column widths.

    Returns:
        Formatted header string.
    """
    if not tasks:
        # Use default widths if no tasks
        header = "ID │ Status │ Priority │ Category │ Due Date     │ Recurs │ Title"
        separator = "───┼────────┼──────────┼──────────┼──────────────┼────────┼───────"
        return f"{header}\n{separator}"

    # Calculate column widths based on content
    id_width = max([len(str(t.id)) for t in tasks], default=2) + 2
    priority_width = max([len(t.priority.value) for t in tasks], default=6) + 2
    category_width = max([len(t.category.value) for t in tasks], default=8) + 2
    due_width = max([len(format_due_datetime(t.due_date, t.due_time)) for t in tasks], default=12)
    recurrence_width = max([len(format_recurrence(t.recurrence)) for t in tasks], default=8)

    # Adjust column widths to fit terminal width if needed
    terminal_width = get_terminal_width()
    title_width = terminal_width - (id_width + 8 + priority_width + 2 + category_width + 2 + due_width + 2 + recurrence_width + 2)
    title_width = max(title_width, 20)  # Minimum title width

    header = (
        f"{'ID':<{id_width}}│ {'Status':<6}│ {'Priority':<{priority_width}}│ "
        f"{'Category':<{category_width}}│ {'Due Date':<{due_width}}│ {'Recurs':<{recurrence_width}}│ {'Title':<{title_width}}"
    )
    separator = (
        f"{'─' * id_width}┼{'─' * 8}┼{'─' * (priority_width + 2)}┼ "
        f"{'─' * (category_width + 2)}┼{'─' * (due_width + 2)}┼{'─' * (recurrence_width + 2)}┼{'─' * title_width}"
    )

    return f"{header}\n{separator}"
