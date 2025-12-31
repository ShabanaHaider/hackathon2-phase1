"""Task entity for the Todo CLI application."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task (auto-assigned by TaskStore).
        title: Short description of the task (required, max 255 chars).
        description: Detailed information about the task (optional, max 2000 chars).
        status: Completion state of the task.
        created_at: Timestamp when the task was created.
        updated_at: Timestamp of the last modification.
    """

    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.INCOMPLETE
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
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=TaskStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
