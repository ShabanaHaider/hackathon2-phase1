"""Unit tests for the Task model."""

import pytest
from datetime import datetime, timezone

from src.models.task import Task, TaskStatus


class TestTaskInitialization:
    """Tests for Task initialization."""

    def test_create_task_with_required_fields(self):
        """Test creating a task with only required fields."""
        task = Task(id=1, title="Buy milk")
        assert task.id == 1
        assert task.title == "Buy milk"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_create_task_with_all_fields(self):
        """Test creating a task with all fields."""
        now = datetime.now(timezone.utc)
        task = Task(
            id=1,
            title="Buy milk",
            description="Get 2% milk from store",
            status=TaskStatus.COMPLETE,
            created_at=now,
            updated_at=now,
        )
        assert task.id == 1
        assert task.title == "Buy milk"
        assert task.description == "Get 2% milk from store"
        assert task.status == TaskStatus.COMPLETE

    def test_default_status_is_incomplete(self):
        """Test that default status is INCOMPLETE."""
        task = Task(id=1, title="Test task")
        assert task.status == TaskStatus.INCOMPLETE


class TestTaskValidation:
    """Tests for Task validation."""

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="")

    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="   ")

    def test_title_too_long_raises_error(self):
        """Test that title exceeding 255 chars raises ValueError."""
        long_title = "x" * 256
        with pytest.raises(ValueError, match="Title exceeds 255 characters"):
            Task(id=1, title=long_title)

    def test_description_too_long_raises_error(self):
        """Test that description exceeding 2000 chars raises ValueError."""
        long_desc = "x" * 2001
        with pytest.raises(ValueError, match="Description exceeds 2000 characters"):
            Task(id=1, title="Test", description=long_desc)


class TestTaskTitleUpdate:
    """Tests for Task title updates."""

    def test_update_title(self):
        """Test updating task title."""
        task = Task(id=1, title="Original")
        original_updated = task.updated_at

        task.update_title("New title")

        assert task.title == "New title"
        assert task.updated_at >= original_updated

    def test_update_title_validates_empty(self):
        """Test that update_title validates empty titles."""
        task = Task(id=1, title="Original")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task.update_title("")

    def test_update_title_trims_whitespace(self):
        """Test that update_title trims whitespace."""
        task = Task(id=1, title="Original")

        task.update_title("  New title  ")

        assert task.title == "New title"

    def test_update_title_too_long_raises_error(self):
        """Test that updating to too-long title raises ValueError."""
        task = Task(id=1, title="Original")
        long_title = "x" * 256

        with pytest.raises(ValueError, match="Title exceeds 255 characters"):
            task.update_title(long_title)


class TestTaskDescriptionUpdate:
    """Tests for Task description updates."""

    def test_update_description(self):
        """Test updating task description."""
        task = Task(id=1, title="Test", description="Original")
        original_updated = task.updated_at

        task.update_description("New description")

        assert task.description == "New description"
        assert task.updated_at >= original_updated

    def test_update_description_too_long_raises_error(self):
        """Test that updating to too-long description raises ValueError."""
        task = Task(id=1, title="Test")
        long_desc = "x" * 2001

        with pytest.raises(ValueError, match="Description exceeds 2000 characters"):
            task.update_description(long_desc)


class TestTaskStatusUpdate:
    """Tests for Task status updates."""

    def test_mark_complete(self):
        """Test marking task as complete."""
        task = Task(id=1, title="Test")
        original_updated = task.updated_at

        task.mark_complete()

        assert task.status == TaskStatus.COMPLETE
        assert task.updated_at >= original_updated

    def test_mark_incomplete(self):
        """Test marking task as incomplete."""
        task = Task(id=1, title="Test", status=TaskStatus.COMPLETE)
        original_updated = task.updated_at

        task.mark_incomplete()

        assert task.status == TaskStatus.INCOMPLETE
        assert task.updated_at >= original_updated


class TestTaskToDict:
    """Tests for Task.to_dict() method."""

    def test_to_dict_contains_all_fields(self):
        """Test that to_dict returns all fields."""
        task = Task(
            id=1,
            title="Test",
            description="Desc",
            status=TaskStatus.COMPLETE,
        )

        task_dict = task.to_dict()

        assert task_dict["id"] == 1
        assert task_dict["title"] == "Test"
        assert task_dict["description"] == "Desc"
        assert task_dict["status"] == "complete"
        assert "created_at" in task_dict
        assert "updated_at" in task_dict


class TestTaskFromDict:
    """Tests for Task.from_dict() classmethod."""

    def test_from_dict_creates_task(self):
        """Test that from_dict creates a task from a dictionary."""
        now = datetime.now(timezone.utc)
        data = {
            "id": 1,
            "title": "Test",
            "description": "Desc",
            "status": "complete",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }

        task = Task.from_dict(data)

        assert task.id == 1
        assert task.title == "Test"
        assert task.description == "Desc"
        assert task.status == TaskStatus.COMPLETE

    def test_from_dict_with_empty_description(self):
        """Test that from_dict handles missing description."""
        now = datetime.now(timezone.utc)
        data = {
            "id": 1,
            "title": "Test",
            "status": "incomplete",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }

        task = Task.from_dict(data)

        assert task.description == ""

    def test_from_dict_roundtrip(self):
        """Test that to_dict and from_dict are inverses."""
        original = Task(
            id=42,
            title="Buy milk",
            description="Get 2% milk",
            status=TaskStatus.COMPLETE,
        )

        task_dict = original.to_dict()
        restored = Task.from_dict(task_dict)

        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.status == original.status
