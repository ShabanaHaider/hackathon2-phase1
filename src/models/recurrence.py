"""Recurrence pattern logic for recurring tasks."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class RecurrenceInterval(Enum):
    """Enumeration of recurrence interval types."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


@dataclass
class RecurrencePattern:
    """Represents a recurrence pattern for repeating tasks.

    Attributes:
        interval_type: Type of recurrence interval.
        interval_value: Number of days for CUSTOM intervals (ignored for others).
    """

    interval_type: RecurrenceInterval
    interval_value: int = 1

    def __post_init__(self) -> None:
        """Validate recurrence pattern after initialization."""
        if self.interval_type == RecurrenceInterval.CUSTOM and self.interval_value <= 0:
            raise ValueError("Custom interval value must be positive")

    def calculate_next_occurrence(self, from_date: datetime) -> datetime:
        """Calculate the next occurrence date based on the recurrence pattern.

        Args:
            from_date: The date to calculate from (typically completion date).

        Returns:
            The next occurrence datetime.
        """
        if self.interval_type == RecurrenceInterval.DAILY:
            return from_date + timedelta(days=1)
        elif self.interval_type == RecurrenceInterval.WEEKLY:
            return from_date + timedelta(days=7)
        elif self.interval_type == RecurrenceInterval.MONTHLY:
            return from_date + timedelta(days=30)
        elif self.interval_type == RecurrenceInterval.CUSTOM:
            return from_date + timedelta(days=self.interval_value)
        else:
            raise ValueError(f"Unsupported recurrence interval: {self.interval_type}")

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "interval_type": self.interval_type.value,
            "interval_value": self.interval_value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RecurrencePattern":
        """Deserialize from dictionary.

        Args:
            data: Dictionary containing recurrence pattern data.

        Returns:
            A new RecurrencePattern instance.
        """
        return cls(
            interval_type=RecurrenceInterval(data["interval_type"]),
            interval_value=data.get("interval_value", 1),
        )

    def __str__(self) -> str:
        """Human-readable representation."""
        if self.interval_type == RecurrenceInterval.DAILY:
            return "Repeats daily"
        elif self.interval_type == RecurrenceInterval.WEEKLY:
            return "Repeats every 7 days"
        elif self.interval_type == RecurrenceInterval.MONTHLY:
            return "Repeats every 30 days"
        elif self.interval_type == RecurrenceInterval.CUSTOM:
            return f"Repeats every {self.interval_value} days"
        else:
            return "Unknown recurrence"
