"""Reminder model for task notifications."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reminder:
    """Represents a scheduled reminder for a task.

    This is an internal model used by ReminderService for notification scheduling.

    Attributes:
        task_id: ID of the task this reminder is for.
        reminder_time: When to trigger the notification.
        minutes_before: How many minutes before due time.
        sent: Whether notification was sent.
    """

    task_id: int
    reminder_time: datetime
    minutes_before: int
    sent: bool = False

    def is_due(self) -> bool:
        """Check if reminder should fire now."""
        return datetime.now() >= self.reminder_time and not self.sent

    def mark_sent(self) -> None:
        """Mark reminder as sent."""
        self.sent = True

    def __lt__(self, other: "Reminder") -> bool:
        """Comparison for priority queue (earlier reminders first)."""
        return self.reminder_time < other.reminder_time
