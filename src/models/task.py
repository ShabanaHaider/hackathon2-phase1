"""Task entity for the Todo CLI application."""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timezone, timedelta
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.recurrence import RecurrencePattern


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


class TaskPriority(Enum):
    """Enumeration of possible task priorities."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskCategory(Enum):
    """Enumeration of possible task categories."""

    WORK = "work"
    HOME = "home"
    UNCATEGORIZED = "uncategorized"


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task (auto-assigned by TaskStore).
        title: Short description of the task (required, max 255 chars).
        description: Detailed information about the task (optional, max 2000 chars).
        status: Completion state of the task.
        priority: Priority level of the task (high/medium/low, default: medium).
        category: Category of the task (work/home/uncategorized, default: uncategorized).
        due_date: Optional due date for the task.
        due_time: Optional time component for due date (requires due_date).
        reminder_intervals: List of reminder intervals in minutes before due time.
        recurrence: Optional recurrence pattern for repeating tasks.
        completed_at: Timestamp when the task was marked complete.
        parent_recurrence_id: ID of parent task if this is a recurring instance.
        created_at: Timestamp when the task was created.
        updated_at: Timestamp of the last modification.
    """

    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.INCOMPLETE
    priority: TaskPriority = TaskPriority.MEDIUM
    category: TaskCategory = TaskCategory.UNCATEGORIZED
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    reminder_intervals: List[int] = field(default_factory=list)
    recurrence: Optional["RecurrencePattern"] = None
    completed_at: Optional[datetime] = None
    parent_recurrence_id: Optional[int] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        """Validate task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 255:
            raise ValueError("Title exceeds 255 characters")
        if len(self.description) > 2000:
            raise ValueError("Description exceeds 2000 characters")

    def update_title(self, new_title: str) -> None:
        """Update the task title and refresh the updated_at timestamp."""
        if not new_title or not new_title.strip():
            raise ValueError("Task title cannot be empty")
        if len(new_title) > 255:
            raise ValueError("Title exceeds 255 characters")
        self.title = new_title.strip()
        self.updated_at = datetime.now(timezone.utc)

    def update_description(self, new_description: str) -> None:
        """Update the task description and refresh the updated_at timestamp."""
        if len(new_description) > 2000:
            raise ValueError("Description exceeds 2000 characters")
        self.description = new_description
        self.updated_at = datetime.now(timezone.utc)

    def update_priority(self, priority: TaskPriority) -> None:
        """Update the task priority and refresh the updated_at timestamp."""
        self.priority = priority
        self.updated_at = datetime.now(timezone.utc)

    def update_category(self, category: TaskCategory) -> None:
        """Update the task category and refresh the updated_at timestamp."""
        self.category = category
        self.updated_at = datetime.now(timezone.utc)

    def update_due_date(self, due_date: Optional[date]) -> None:
        """Update the task due date and refresh the updated_at timestamp."""
        self.due_date = due_date
        self.updated_at = datetime.now(timezone.utc)


    def update_due_time(self, due_time: Optional[time]) -> None:
        """Update the task due time. Requires due_date to be set."""
        if due_time is not None and self.due_date is None:
            raise ValueError("Cannot set due_time without due_date")
        self.due_time = due_time
        self.updated_at = datetime.now(timezone.utc)


    def update_recurrence(self, recurrence: Optional["RecurrencePattern"]) -> None:
        """Update the task recurrence pattern."""
        self.recurrence = recurrence
        self.updated_at = datetime.now(timezone.utc)


    def set_reminder_intervals(self, intervals: List[int]) -> None:
        """Set reminder intervals (minutes before due time)."""
        if self.due_date is None:
            raise ValueError("Cannot set reminders without due_date")
        if len(intervals) > 5:
            raise ValueError("Maximum 5 reminders per task")
        if any(i <= 0 for i in intervals):
            raise ValueError("Reminder intervals must be positive")
        self.reminder_intervals = sorted(intervals, reverse=True)  # Largest first
        self.updated_at = datetime.now(timezone.utc)


    def get_full_due_datetime(self) -> Optional[datetime]:
        """Combine due_date and due_time into a full datetime (local timezone)."""
        if self.due_date is None:
            return None
        time_component = self.due_time or time(23, 59, 59)
        return datetime.combine(self.due_date, time_component)


    def is_overdue(self) -> bool:
        """Check if task is overdue (past due date/time and not complete)."""
        if self.status == TaskStatus.COMPLETE:
            return False
        due_dt = self.get_full_due_datetime()
        if due_dt is None:
            return False
        return datetime.now() > due_dt


    def calculate_reminder_times(self) -> List[datetime]:
        """Calculate absolute times when reminders should fire."""
        due_dt = self.get_full_due_datetime()
        if due_dt is None or not self.reminder_intervals:
            return []
        return [due_dt - timedelta(minutes=interval) for interval in self.reminder_intervals]

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.status = TaskStatus.COMPLETE
        self.completed_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.status = TaskStatus.INCOMPLETE
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "category": self.category.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "due_time": self.due_time.isoformat() if self.due_time else None,
            "reminder_intervals": self.reminder_intervals,
            "recurrence": self.recurrence.to_dict() if self.recurrence else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "parent_recurrence_id": self.parent_recurrence_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task from a dictionary representation.

        Args:
            data: Dictionary containing task data.

        Returns:
            A new Task instance.
        """
        # Import here to avoid circular dependency
        from src.models.recurrence import RecurrencePattern

        # Handle legacy tasks without new fields
        priority_value = data.get("priority", "medium")
        category_value = data.get("category", "uncategorized")
        due_date_str = data.get("due_date")
        due_time_str = data.get("due_time")
        completed_at_str = data.get("completed_at")

        # Parse priority
        if isinstance(priority_value, str):
            priority = TaskPriority(priority_value)
        else:
            priority = TaskPriority.MEDIUM

        # Parse category
        if isinstance(category_value, str):
            category = TaskCategory(category_value)
        else:
            category = TaskCategory.UNCATEGORIZED

        # Parse due date
        due_date = date.fromisoformat(due_date_str) if due_date_str else None

        # Parse due time
        due_time = time.fromisoformat(due_time_str) if due_time_str else None

        # Parse status
        status_value = data.get("status", "incomplete")
        if isinstance(status_value, str):
            status = TaskStatus(status_value)
        else:
            status = TaskStatus.INCOMPLETE

        # Parse reminder intervals
        reminder_intervals = data.get("reminder_intervals", [])

        # Parse recurrence pattern
        recurrence_data = data.get("recurrence")
        recurrence = RecurrencePattern.from_dict(recurrence_data) if recurrence_data else None

        # Parse completed_at
        completed_at = datetime.fromisoformat(completed_at_str) if completed_at_str else None

        # Parse parent_recurrence_id
        parent_recurrence_id = data.get("parent_recurrence_id")

        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=status,
            priority=priority,
            category=category,
            due_date=due_date,
            due_time=due_time,
            reminder_intervals=reminder_intervals,
            recurrence=recurrence,
            completed_at=completed_at,
            parent_recurrence_id=parent_recurrence_id,
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
