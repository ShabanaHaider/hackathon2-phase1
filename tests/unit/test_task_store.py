"""Unit tests for the TaskStore."""

import pytest

from src.models.task import Task, TaskStatus
from src.storage.task_store import TaskNotFoundError, TaskStore


@pytest.fixture
def fresh_store():
    """Create a fresh TaskStore with cleared storage for each test."""
    return TaskStore(clear_on_init=True)


class TestTaskStoreInitialization:
    """Tests for TaskStore initialization."""

    def test_initializes_empty(self, fresh_store):
        """Test that new TaskStore is empty."""
        assert fresh_store.count() == 0

    def test_next_id_starts_at_1(self, fresh_store):
        """Test that first task gets ID 1."""
        task = fresh_store.add("Task 1")
        assert task.id == 1


class TestTaskStoreAdd:
    """Tests for TaskStore.add() method."""

    def test_add_single_task(self, fresh_store):
        """Test adding a single task."""
        task = fresh_store.add("Buy milk")

        assert fresh_store.count() == 1
        assert task.title == "Buy milk"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE

    def test_add_task_with_description(self, fresh_store):
        """Test adding a task with description."""
        task = fresh_store.add("Buy milk", "Get 2% milk")

        assert task.description == "Get 2% milk"

    def test_add_multiple_tasks_increments_ids(self, fresh_store):
        """Test that adding multiple tasks increments IDs."""
        task1 = fresh_store.add("Task 1")
        task2 = fresh_store.add("Task 2")
        task3 = fresh_store.add("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_validates_empty_title(self, fresh_store):
        """Test that add validates empty title."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            fresh_store.add("")

    def test_add_validates_title_length(self, fresh_store):
        """Test that add validates title length."""
        long_title = "x" * 256

        with pytest.raises(ValueError, match="Title exceeds 255 characters"):
            fresh_store.add(long_title)

    def test_add_validates_description_length(self, fresh_store):
        """Test that add validates description length."""
        long_desc = "x" * 2001

        with pytest.raises(ValueError, match="Description exceeds 2000 characters"):
            fresh_store.add("Test", long_desc)


class TestTaskStoreGet:
    """Tests for TaskStore retrieval methods."""

    def test_get_existing_task(self, fresh_store):
        """Test retrieving an existing task."""
        fresh_store.add("Task 1")
        task = fresh_store.get(1)

        assert task is not None
        assert task.title == "Task 1"

    def test_get_nonexistent_task(self, fresh_store):
        """Test retrieving a non-existent task returns None."""
        task = fresh_store.get(999)

        assert task is None

    def test_get_all_empty(self, fresh_store):
        """Test getting all tasks when empty."""
        tasks = fresh_store.get_all()

        assert tasks == []

    def test_get_all_multiple_tasks(self, fresh_store):
        """Test getting all tasks returns them in order."""
        fresh_store.add("Task 1")
        fresh_store.add("Task 2")
        fresh_store.add("Task 3")

        tasks = fresh_store.get_all()

        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_get_by_id_or_raise_existing(self, fresh_store):
        """Test get_by_id_or_raise with existing task."""
        fresh_store.add("Task 1")
        task = fresh_store.get_by_id_or_raise(1)

        assert task.title == "Task 1"

    def test_get_by_id_or_raise_nonexistent(self, fresh_store):
        """Test get_by_id_or_raise with non-existent task raises error."""
        with pytest.raises(TaskNotFoundError):
            fresh_store.get_by_id_or_raise(999)


class TestTaskStoreUpdate:
    """Tests for TaskStore.update() method."""

    def test_update_title(self, fresh_store):
        """Test updating task title."""
        fresh_store.add("Original")
        task = fresh_store.update(1, title="Updated")

        assert task.title == "Updated"

    def test_update_description(self, fresh_store):
        """Test updating task description."""
        fresh_store.add("Task", "Original")
        task = fresh_store.update(1, description="Updated")

        assert task.description == "Updated"

    def test_update_both_fields(self, fresh_store):
        """Test updating both title and description."""
        fresh_store.add("Original", "Original desc")
        task = fresh_store.update(1, title="New", description="New desc")

        assert task.title == "New"
        assert task.description == "New desc"

    def test_update_nonexistent_task(self, fresh_store):
        """Test updating non-existent task raises error."""
        with pytest.raises(TaskNotFoundError):
            fresh_store.update(999, title="New")

    def test_update_no_changes_raises_error(self, fresh_store):
        """Test that update with no changes raises error."""
        fresh_store.add("Task")

        with pytest.raises(ValueError, match="No changes provided"):
            fresh_store.update(1)


class TestTaskStoreDelete:
    """Tests for TaskStore.delete() method."""

    def test_delete_existing_task(self, fresh_store):
        """Test deleting an existing task."""
        fresh_store.add("Task 1")
        fresh_store.add("Task 2")

        result = fresh_store.delete(1)

        assert result is True
        assert fresh_store.count() == 1
        assert fresh_store.get(1) is None

    def test_delete_nonexistent_task(self, fresh_store):
        """Test deleting non-existent task returns False."""
        fresh_store.add("Task 1")

        result = fresh_store.delete(999)

        assert result is False
        assert fresh_store.count() == 1

    def test_delete_updates_id_sequence(self, fresh_store):
        """Test that deleting doesn't affect next_id."""
        fresh_store.add("Task 1")
        fresh_store.add("Task 2")
        fresh_store.delete(1)
        new_task = fresh_store.add("Task 3")

        assert new_task.id == 3


class TestTaskStoreMarkStatus:
    """Tests for TaskStore status marking methods."""

    def test_mark_complete(self, fresh_store):
        """Test marking task as complete."""
        fresh_store.add("Task")
        task = fresh_store.mark_complete(1)

        assert task.status == TaskStatus.COMPLETE

    def test_mark_incomplete(self, fresh_store):
        """Test marking task as incomplete."""
        fresh_store.add("Task")
        fresh_store.mark_complete(1)  # First mark complete
        task = fresh_store.mark_incomplete(1)

        assert task.status == TaskStatus.INCOMPLETE

    def test_mark_complete_nonexistent(self, fresh_store):
        """Test marking non-existent task as complete raises error."""
        with pytest.raises(TaskNotFoundError):
            fresh_store.mark_complete(999)

    def test_mark_incomplete_nonexistent(self, fresh_store):
        """Test marking non-existent task as incomplete raises error."""
        with pytest.raises(TaskNotFoundError):
            fresh_store.mark_incomplete(999)


class TestTaskStoreCountAndClear:
    """Tests for TaskStore count and clear methods."""

    def test_count(self, fresh_store):
        """Test counting tasks."""
        fresh_store.add("Task 1")
        fresh_store.add("Task 2")

        assert fresh_store.count() == 2

    def test_clear(self, fresh_store):
        """Test clearing all tasks."""
        fresh_store.add("Task 1")
        fresh_store.add("Task 2")

        fresh_store.clear()

        assert fresh_store.count() == 0
        task = fresh_store.add("Task 1")
        assert task.id == 1  # ID sequence resets
