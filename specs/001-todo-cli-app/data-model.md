# Data Model: Todo CLI Application

**Feature**: 001-todo-cli-app
**Created**: 2025-12-30
**Based on**: [spec.md](../001-todo-cli-app/spec.md)

## Entities

### Task

Represents a single todo item managed by the user.

#### Attributes

| Attribute | Type | Required | Default | Validation |
|-----------|------|----------|---------|------------|
| `id` | Integer | Yes | Auto-increment (1, 2, 3...) | Unique within session |
| `title` | String | Yes | N/A | Non-empty, max 255 chars |
| `description` | String | No | Empty string | Max 2000 chars |
| `status` | Enum | Yes | `incomplete` | `incomplete` or `complete` |
| `created_at` | DateTime | Yes | Current timestamp | ISO 8601 format |
| `updated_at` | DateTime | Yes | Current timestamp | ISO 8601 format |

#### State Transitions

```
incomplete <--[mark complete]--> complete
     ^                            |
     |                            v
     +-------[mark incomplete]----+
```

A task can transition between `incomplete` and `complete` states via the mark complete/incomplete commands.

#### Constraints

1. Task IDs are unique within a session and never reused after deletion
2. Title must not be empty or whitespace-only
3. Timestamps are updated on any modification (title, description, or status)
4. Deleted tasks are removed from memory entirely

#### Relationships

- **Task Store**: Container that holds all Task instances
- **1:N**: One Task Store contains many Tasks

## Storage

### TaskStore

In-memory container for all tasks.

#### Responsibilities

- Maintain task collection in memory
- Generate unique task IDs
- Provide CRUD operations for tasks
- Track next available ID

#### Data Structure

```python
# Conceptual (implementation detail hidden from spec)
tasks: List[Task]  # Ordered by creation
next_id: int       # Auto-incrementing counter
```

#### Operations

| Operation | Parameters | Returns | Side Effects |
|-----------|------------|---------|--------------|
| `add()` | title: str, description: str | Task | Adds task to collection |
| `get()` | task_id: int | Task or None | None if not found |
| `get_all()` | None | List[Task] | Returns ordered by ID |
| `update()` | task_id: int, title: str, description: str | Task | Updates task fields |
| `delete()` | task_id: int | bool | Removes task, returns success |
| `mark_complete()` | task_id: int | Task | Updates status to complete |
| `mark_incomplete()` | task_id: int | Task | Updates status to incomplete |

---

**End of Data Model**
