"""Recurrence service for creating recurring task instances."""

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.task import Task
    from src.storage.task_store import TaskStore


class RecurrenceService:
    """Service for handling recurring task instance creation."""

    def create_next_instance(
        self, completed_task: "Task", task_store: "TaskStore"
    ) -> "Task":
        """Create next instance of a recurring task after completion.

        Args:
            completed_task: The task that was just completed.
            task_store: TaskStore to add the new instance to.

        Returns:
            The newly created task instance.

        Raises:
            ValueError: If task is not recurring.
        """
        if completed_task.recurrence is None:
            raise ValueError("Task is not recurring")

        # Calculate next occurrence date
        completed_at = completed_task.completed_at or datetime.now()
        next_due = completed_task.recurrence.calculate_next_occurrence(completed_at)

        # Create new task instance with same properties
        new_task = task_store.add(
            title=completed_task.title,
            description=completed_task.description,
            priority=completed_task.priority,
            category=completed_task.category,
        )

        # Set recurrence-specific properties
        new_task.recurrence = completed_task.recurrence
        new_task.parent_recurrence_id = completed_task.id
        new_task.reminder_intervals = completed_task.reminder_intervals[:]  # Copy the list

        # Set due date/time based on the next occurrence
        from datetime import date
        new_task.due_date = next_due.date()
        new_task.due_time = completed_task.due_time  # Preserve the time if it existed

        return new_task
