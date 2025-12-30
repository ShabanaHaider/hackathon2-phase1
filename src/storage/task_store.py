"""In-memory task storage for the Todo CLI application."""

from typing import Dict, List, Optional

from src.models.task import Task, TaskStatus


class TaskNotFoundError(Exception):
    """Raised when a task with the given ID is not found."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found")


class TaskStore:
    """In-memory storage for tasks.

    Maintains a collection of tasks in memory with unique ID assignment.

    Attributes:
        tasks: Dictionary mapping task IDs to Task objects.
        next_id: The next available task ID for new tasks.
    """

    def __init__(self) -> None:
        """Initialize an empty task store."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        """Add a new task to the store.

        Args:
            title: The task title (required).
            description: The task description (optional).

        Returns:
            The newly created Task.

        Raises:
            ValueError: If title is empty or too long.
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        if len(title) > 255:
            raise ValueError("Title exceeds 255 characters")
        if len(description) > 2000:
            raise ValueError("Description exceeds 2000 characters")

        task_id = self._next_id
        task = Task(
            id=task_id,
            title=title.strip(),
            description=description,
            status=TaskStatus.INCOMPLETE,
        )
        self._tasks[task_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def get_by_id_or_raise(self, task_id: int) -> Task:
        """Retrieve a task by ID or raise TaskNotFoundError.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task if found.

        Raises:
            TaskNotFoundError: If the task is not found.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def get_all(self) -> List[Task]:
        """Get all tasks ordered by ID.

        Returns:
            List of all tasks ordered by creation order.
        """
        return [self._tasks[task_id] for task_id in sorted(self._tasks.keys())]

    def update(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (optional).
            description: New description (optional).

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If the task is not found.
            ValueError: If no changes provided or validation fails.
        """
        if title is None and description is None:
            raise ValueError("No changes provided (use --title and/or --description)")

        task = self.get_by_id_or_raise(task_id)

        if title is not None:
            task.update_title(title)
        if description is not None:
            task.update_description(description)

        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was deleted, False if not found.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If the task is not found.
        """
        task = self.get_by_id_or_raise(task_id)
        task.mark_complete()
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If the task is not found.
        """
        task = self.get_by_id_or_raise(task_id)
        task.mark_incomplete()
        return task

    def count(self) -> int:
        """Return the number of tasks in the store."""
        return len(self._tasks)

    def clear(self) -> None:
        """Remove all tasks from the store."""
        self._tasks.clear()
        self._next_id = 1
