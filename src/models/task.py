"""Task entity for the Todo CLI application."""

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional


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

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.status = TaskStatus.COMPLETE
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
        # Handle legacy tasks without new fields
        priority_value = data.get("priority", "medium")
        category_value = data.get("category", "uncategorized")
        due_date_str = data.get("due_date")

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

        # Parse status
        status_value = data.get("status", "incomplete")
        if isinstance(status_value, str):
            status = TaskStatus(status_value)
        else:
            status = TaskStatus.INCOMPLETE

        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=status,
            priority=priority,
            category=category,
            due_date=due_date,
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
