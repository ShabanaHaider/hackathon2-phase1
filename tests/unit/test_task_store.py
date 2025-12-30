"""Unit tests for the TaskStore."""

import pytest

from src.models.task import Task, TaskStatus
from src.storage.task_store import TaskNotFoundError, TaskStore


class TestTaskStoreInitialization:
    """Tests for TaskStore initialization."""

    def test_initializes_empty(self):
        """Test that new TaskStore is empty."""
        store = TaskStore()
        assert store.count() == 0

    def test_next_id_starts_at_1(self):
        """Test that first task gets ID 1."""
        store = TaskStore()
        task = store.add("Task 1")
        assert task.id == 1


class TestTaskStoreAdd:
    """Tests for TaskStore.add() method."""

    def test_add_single_task(self):
        """Test adding a single task."""
        store = TaskStore()
        task = store.add("Buy milk")

        assert store.count() == 1
        assert task.title == "Buy milk"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE

    def test_add_task_with_description(self):
        """Test adding a task with description."""
        store = TaskStore()
        task = store.add("Buy milk", "Get 2% milk")

        assert task.description == "Get 2% milk"

    def test_add_multiple_tasks_increments_ids(self):
        """Test that adding multiple tasks increments IDs."""
        store = TaskStore()
        task1 = store.add("Task 1")
        task2 = store.add("Task 2")
        task3 = store.add("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_validates_empty_title(self):
        """Test that add validates empty title."""
        store = TaskStore()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            store.add("")

    def test_add_validates_title_length(self):
        """Test that add validates title length."""
        store = TaskStore()
        long_title = "x" * 256

        with pytest.raises(ValueError, match="Title exceeds 255 characters"):
            store.add(long_title)

    def test_add_validates_description_length(self):
        """Test that add validates description length."""
        store = TaskStore()
        long_desc = "x" * 2001

        with pytest.raises(ValueError, match="Description exceeds 2000 characters"):
            store.add("Test", long_desc)


class TestTaskStoreGet:
    """Tests for TaskStore retrieval methods."""

    def test_get_existing_task(self):
        """Test retrieving an existing task."""
        store = TaskStore()
        store.add("Task 1")
        task = store.get(1)

        assert task is not None
        assert task.title == "Task 1"

    def test_get_nonexistent_task(self):
        """Test retrieving a non-existent task returns None."""
        store = TaskStore()
        task = store.get(999)

        assert task is None

    def test_get_all_empty(self):
        """Test getting all tasks when empty."""
        store = TaskStore()
        tasks = store.get_all()

        assert tasks == []

    def test_get_all_multiple_tasks(self):
        """Test getting all tasks returns them in order."""
        store = TaskStore()
        store.add("Task 1")
        store.add("Task 2")
        store.add("Task 3")

        tasks = store.get_all()

        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_get_by_id_or_raise_existing(self):
        """Test get_by_id_or_raise with existing task."""
        store = TaskStore()
        store.add("Task 1")
        task = store.get_by_id_or_raise(1)

        assert task.title == "Task 1"

    def test_get_by_id_or_raise_nonexistent(self):
        """Test get_by_id_or_raise with non-existent task raises error."""
        store = TaskStore()

        with pytest.raises(TaskNotFoundError):
            store.get_by_id_or_raise(999)


class TestTaskStoreUpdate:
    """Tests for TaskStore.update() method."""

    def test_update_title(self):
        """Test updating task title."""
        store = TaskStore()
        store.add("Original")
        task = store.update(1, title="Updated")

        assert task.title == "Updated"

    def test_update_description(self):
        """Test updating task description."""
        store = TaskStore()
        store.add("Task", "Original")
        task = store.update(1, description="Updated")

        assert task.description == "Updated"

    def test_update_both_fields(self):
        """Test updating both title and description."""
        store = TaskStore()
        store.add("Original", "Original desc")
        task = store.update(1, title="New", description="New desc")

        assert task.title == "New"
        assert task.description == "New desc"

    def test_update_nonexistent_task(self):
        """Test updating non-existent task raises error."""
        store = TaskStore()

        with pytest.raises(TaskNotFoundError):
            store.update(999, title="New")

    def test_update_no_changes_raises_error(self):
        """Test that update with no changes raises error."""
        store = TaskStore()
        store.add("Task")

        with pytest.raises(ValueError, match="No changes provided"):
            store.update(1)


class TestTaskStoreDelete:
    """Tests for TaskStore.delete() method."""

    def test_delete_existing_task(self):
        """Test deleting an existing task."""
        store = TaskStore()
        store.add("Task 1")
        store.add("Task 2")

        result = store.delete(1)

        assert result is True
        assert store.count() == 1
        assert store.get(1) is None

    def test_delete_nonexistent_task(self):
        """Test deleting non-existent task returns False."""
        store = TaskStore()
        store.add("Task 1")

        result = store.delete(999)

        assert result is False
        assert store.count() == 1

    def test_delete_updates_id_sequence(self):
        """Test that deleting doesn't affect next_id."""
        store = TaskStore()
        store.add("Task 1")
        store.add("Task 2")
        store.delete(1)
        new_task = store.add("Task 3")

        assert new_task.id == 3


class TestTaskStoreMarkStatus:
    """Tests for TaskStore status marking methods."""

    def test_mark_complete(self):
        """Test marking task as complete."""
        store = TaskStore()
        store.add("Task")
        task = store.mark_complete(1)

        assert task.status == TaskStatus.COMPLETE

    def test_mark_incomplete(self):
        """Test marking task as incomplete."""
        store = TaskStore()
        task = store.add("Task")
        store.mark_complete(1)  # First mark complete
        task = store.mark_incomplete(1)

        assert task.status == TaskStatus.INCOMPLETE

    def test_mark_complete_nonexistent(self):
        """Test marking non-existent task as complete raises error."""
        store = TaskStore()

        with pytest.raises(TaskNotFoundError):
            store.mark_complete(999)

    def test_mark_incomplete_nonexistent(self):
        """Test marking non-existent task as incomplete raises error."""
        store = TaskStore()

        with pytest.raises(TaskNotFoundError):
            store.mark_incomplete(999)


class TestTaskStoreCountAndClear:
    """Tests for TaskStore count and clear methods."""

    def test_count(self):
        """Test counting tasks."""
        store = TaskStore()
        store.add("Task 1")
        store.add("Task 2")

        assert store.count() == 2

    def test_clear(self):
        """Test clearing all tasks."""
        store = TaskStore()
        store.add("Task 1")
        store.add("Task 2")

        store.clear()

        assert store.count() == 0
        task = store.add("Task 1")
        assert task.id == 1  # ID sequence resets
