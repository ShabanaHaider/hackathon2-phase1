# Data Model: Task Management CLI Enhancements

**Feature**: Task Management CLI Enhancements
**Created**: 2026-01-01
**Based On**: Feature specification (`spec.md`)

## Overview

This document defines the data entities, validation rules, and state transitions required for the task management CLI enhancements. The design extends the existing Task model with priority, category, and due date fields while maintaining backward compatibility.

## Entities

### TaskPriority (Enumeration)

Represents the priority level of a task.

```python
class TaskPriority(Enum):
    """Enumeration of possible task priorities."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

**Rules**:
- Only three valid values: high, medium, low
- Default priority is MEDIUM
- Order for sorting: HIGH > MEDIUM > LOW

### TaskCategory (Enumeration)

Represents the category of a task.

```python
class TaskCategory(Enum):
    """Enumeration of possible task categories."""

    WORK = "work"
    HOME = "home"
    UNCATEGORIZED = "uncategorized"
```

**Rules**:
- Valid values: work, home, uncategorized
- Default category is UNCATEGORIZED
- Case-insensitive matching for input

### TaskStatus (Existing)

Already defined in the codebase. Preserved for backward compatibility.

```python
class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
```

### Task (Extended)

Represents a single todo task with all enhanced attributes.

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional

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
```

**Validation Rules**:
- Title cannot be empty or whitespace-only
- Title must not exceed 255 characters
- Description must not exceed 2000 characters
- Due date format: YYYY-MM-DD (validated at CLI input)

### TaskFilter (Data Class)

Criteria for filtering tasks.

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class TaskFilter:
    """Criteria for filtering tasks."""

    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    category: Optional[TaskCategory] = None
```

### TaskSort (Data Class)

Criteria for sorting tasks.

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TaskSortBy(Enum):
    """Sort options for tasks."""

    DUE_DATE = "due_date"
    PRIORITY = "priority"
    TITLE = "title"

class TaskSortOrder(Enum):
    """Sort order options."""

    ASC = "asc"
    DESC = "desc"

@dataclass
class TaskSort:
    """Criteria for sorting tasks."""

    by: TaskSortBy
    order: TaskSortOrder = TaskSortOrder.ASC
```

## Storage Format

### JSON Schema for Task Persistence

```json
{
  "next_id": 1,
  "tasks": {
    "1": {
      "id": 1,
      "title": "Buy milk",
      "description": "Get 2% milk from the store",
      "status": "incomplete",
      "priority": "high",
      "category": "home",
      "due_date": "2026-01-15",
      "created_at": "2026-01-01T10:00:00+00:00",
      "updated_at": "2026-01-01T10:00:00+00:00"
    }
  }
}
```

**Notes**:
- `due_date` is stored as ISO 8601 date string (YYYY-MM-DD) or null
- `priority` and `category` stored as lowercase strings matching enum values
- Existing tasks without new fields will default to: priority=medium, category=uncategorized, due_date=null

## Validation Rules

### Input Validation (CLI)

| Field | Valid Values | Invalid Values | Error Message |
|-------|--------------|----------------|---------------|
| priority | high, medium, low (case-insensitive) | any other value | "Invalid priority. Must be high, medium, or low." |
| category | work, home (case-insensitive) | any other value | "Invalid category. Must be work or home." |
| due_date | YYYY-MM-DD format | any other format | "Invalid date format. Use YYYY-MM-DD." |

### Business Logic Validation

- Due date can be any valid date (past, present, or future)
- No restrictions on due dates (users can set past dates if desired)
- Tasks can have no due date (null/None)
- Category is case-insensitive in input but stored lowercase

## State Transitions

### Task Status Transitions

```
INCOMPLETE <---> COMPLETE
    ^               |
    |_______________|
   (toggle via complete/incomplete commands)
```

### Task Attribute Updates

Attributes that can be updated independently:
- title (always)
- description (always)
- priority (always)
- category (always)
- due_date (can be set or cleared to null)

## Relationships

```
TaskStore (1) ----> (N) Task
  |
  +-- manages: task lifecycle (add, update, delete)
  +-- provides: filtering and sorting
  +-- persists: to JSON file at ~/.todo/tasks.json
```

## Backward Compatibility

### Handling Legacy Tasks

When loading tasks from storage that don't have the new fields:

```python
# In Task.from_dict()
priority = TaskPriority(data.get("priority", "medium"))
category = TaskCategory(data.get("category", "uncategorized"))
due_date_str = data.get("due_date")
due_date = date.fromisoformat(due_date_str) if due_date_str else None
```

### Default Values

| Field | Default Value | Rationale |
|-------|---------------|-----------|
| priority | MEDIUM | Neutral priority for legacy tasks |
| category | UNCATEGORIZED | Users can categorize later |
| due_date | None | No due date set |

## Related Artifacts

- `spec.md`: Feature specification with user stories
- `plan.md`: Implementation plan and technical decisions
- `contracts/cli-commands.md`: CLI command signatures
- `quickstart.md`: Usage guide
