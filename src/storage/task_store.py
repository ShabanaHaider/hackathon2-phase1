"""In-memory task storage for the Todo CLI application."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from src.models.task import Task, TaskStatus


class TaskNotFoundError(Exception):
    """Raised when a task with the given ID is not found."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found")


# Default storage file path (user's home directory)
DEFAULT_STORAGE_DIR = Path.home() / ".todo"
DEFAULT_STORAGE_FILE = DEFAULT_STORAGE_DIR / "tasks.json"


class TaskStore:
    """In-memory storage for tasks with file-based persistence.

    Maintains a collection of tasks in memory with unique ID assignment.
    Tasks are automatically persisted to a JSON file for durability.

    Attributes:
        tasks: Dictionary mapping task IDs to Task objects.
        next_id: The next available task ID for new tasks.
        storage_file: Path to the JSON file for persistence.
    """

    def __init__(self, storage_file: Optional[Path] = None, clear_on_init: bool = False) -> None:
        """Initialize an empty task store.

        Args:
            storage_file: Optional path to the storage file. Defaults to ~/.todo/tasks.json
            clear_on_init: If True, clear the storage file on initialization (for testing).
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._storage_file = storage_file or DEFAULT_STORAGE_FILE

        # Clear storage if requested (for testing)
        if clear_on_init and self._storage_file.exists():
            try:
                os.remove(self._storage_file)
            except OSError:
                pass

        self._load()

    def _load(self) -> None:
        """Load tasks from the JSON storage file."""
        if self._storage_file.exists():
            try:
                with open(self._storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._next_id = data.get("next_id", 1)
                    tasks_data = data.get("tasks", {})
                    self._tasks = {
                        int(task_id): Task.from_dict(task_data)
                        for task_id, task_data in tasks_data.items()
                    }
            except (json.JSONDecodeError, OSError, KeyError, TypeError):
                # If file is corrupted or unreadable, start fresh
                self._tasks = {}
                self._next_id = 1

    def _save(self) -> None:
        """Save tasks to the JSON storage file atomically."""
        # Ensure storage directory exists
        self._storage_file.parent.mkdir(parents=True, exist_ok=True)

        # Write to a temporary file first, then rename for atomicity
        temp_file = self._storage_file.with_suffix(".tmp")
        data = {
            "next_id": self._next_id,
            "tasks": {str(task_id): task.to_dict() for task_id, task in self._tasks.items()},
        }
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            # Atomic rename on Windows
            temp_file.replace(self._storage_file)
        except OSError:
            # If atomic rename fails, try direct write
            with open(self._storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

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
        self._save()
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

        self._save()
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
            self._save()
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
        self._save()
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
        self._save()
        return task

    def count(self) -> int:
        """Return the number of tasks in the store."""
        return len(self._tasks)

    def clear(self) -> None:
        """Remove all tasks from the store."""
        self._tasks.clear()
        self._next_id = 1
        self._save()
