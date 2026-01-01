# CLI Command Contracts: Task Management CLI Enhancements

**Feature**: Task Management CLI Enhancements
**Created**: 2026-01-01
**Based On**: Feature specification (`spec.md`) and Data model (`data-model.md`)

## Overview

This document defines the CLI command contracts for the task management enhancements. All commands are implemented using Click and follow the existing patterns in the codebase.

## Command Group

### `todo`

The main command group for the Todo CLI application.

```bash
todo --version
todo --help
```

**Options**:
- `--version, -V`: Show version and exit
- `--help`: Show help message

---

## Command: `add`

Adds a new task to the todo list with optional priority, category, and due date.

### Signature

```bash
todo add "Task title" [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `title` | positional | required | Task title (1-255 characters) |
| `--description, -d` | string | "" | Task description (optional) |
| `--priority, -p` | choice | medium | Priority level (high/medium/low) |
| `--category, -c` | choice | uncategorized | Category (work/home) |
| `--due-date, -D` | string | None | Due date in YYYY-MM-DD format |

### Examples

```bash
# Basic task with defaults
todo add "Buy milk"

# Full task with all options
todo add "Finish report" --priority high --category work --due-date 2026-01-15

# Task with description
todo add "Call mom" --description "Wish her happy birthday" --category home
```

### Input Validation

- Title cannot be empty
- Title cannot exceed 255 characters
- Description cannot exceed 2000 characters
- Priority must be one of: high, medium, low (case-insensitive)
- Category must be one of: work, home (case-insensitive)
- Due date must be in YYYY-MM-DD format

### Success Output

```
Added task 1: Buy milk
```

### Error Output

```
Error: Invalid priority. Must be high, medium, or low.
Error: Invalid date format. Use YYYY-MM-DD.
Error: Task title cannot be empty
```

---

## Command: `list`

Lists all tasks with optional filtering and sorting.

### Signature

```bash
todo list [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--status, -s` | choice | None | Filter by status (pending/completed) |
| `--priority, -p` | choice | None | Filter by priority (high/medium/low) |
| `--category, -c` | choice | None | Filter by category (work/home) |
| `--filter-by` | string | None | Legacy filter option (status/priority/category) |
| `--sort-by` | choice | None | Sort by (due_date/priority/title) |
| `--sort-order` | choice | asc | Sort order (asc/desc) |

### Examples

```bash
# List all tasks
todo list

# Filter by status
todo list --status pending
todo list --status completed

# Filter by priority
todo list --priority high

# Filter by category
todo list --category work

# Combine filters
todo list --priority high --category work

# Sort by due date
todo list --sort-by due_date

# Sort by priority
todo list --sort-by priority

# Sort by title (alphabetical)
todo list --sort-by title

# Sort in descending order
todo list --sort-by title --sort-order desc
```

### Output Format

```
ID  | Status    | Title          | Priority | Category | Due Date
----|-----------|----------------|----------|----------|------------
1   | [ ]       | Buy milk       | high     | home     | 2026-01-15
2   | [ ]       | Finish report  | high     | work     | 2026-01-20
3   | [x]       | Call mom       | low      | home     |
```

### Empty State

```
No tasks found. Add a task with: todo add "Task name"
```

### No Matching Tasks

```
No tasks found matching the specified filters.
```

---

## Command: `update`

Updates an existing task's attributes.

### Signature

```bash
todo update <TASK_ID> [OPTIONS]
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `task_id` | integer | The ID of the task to update |

### Options

| Option | Type | Description |
|--------|------|-------------|
| `--title, -t` | string | New task title |
| `--description, -d` | string | New task description |
| `--priority, -p` | choice | New priority (high/medium/low) |
| `--category, -c` | choice | New category (work/home) |
| `--due-date, -D` | string | New due date (YYYY-MM-DD) or empty to clear |

### Examples

```bash
# Update title only
todo update 1 --title "Buy 2% milk"

# Update priority
todo update 1 --priority high

# Update category
todo update 1 --category work

# Update due date
todo update 1 --due-date 2026-02-01

# Clear due date
todo update 1 --due-date ""

# Update multiple attributes
todo update 1 --priority high --due-date 2026-01-20
```

### Input Validation

- Task ID must exist
- Title cannot be empty or exceed 255 characters
- Priority must be one of: high, medium, low
- Category must be one of: work, home
- Due date must be in YYYY-MM-DD format or empty string

### Success Output

```
Updated task 1: Buy 2% milk
```

### Error Output

```
Error: Task 1 not found.
Error: No changes provided. Use at least one of: --title, --description, --priority, --category, --due-date
```

---

## Command: `delete`

Deletes a task from the todo list.

### Signature

```bash
todo delete <TASK_ID>
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `task_id` | integer | The ID of the task to delete |

### Examples

```bash
todo delete 1
```

### Success Output

```
Deleted task 1.
```

### Error Output

```
Error: Task 1 not found.
```

---

## Command: `complete`

Marks a task as complete.

### Signature

```bash
todo complete <TASK_ID>
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `task_id` | integer | The ID of the task to complete |

### Examples

```bash
todo complete 1
```

### Success Output

```
Completed task 1: Buy milk
```

### Error Output

```
Error: Task 1 not found.
```

---

## Command: `incomplete`

Marks a task as incomplete (pending).

### Signature

```bash
todo incomplete <TASK_ID>
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `task_id` | integer | The ID of the task to mark incomplete |

### Examples

```bash
todo incomplete 1
```

### Success Output

```
Marked task 1 as incomplete: Buy milk
```

### Error Output

```
Error: Task 1 not found.
```

---

## Global Options

All commands support these global options:

| Option | Description |
|--------|-------------|
| `--help, -h` | Show help message |
| `--version, -V` | Show version information |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid input, task not found, etc.) |

---

## Backward Compatibility

All existing commands continue to work without modification:

- `todo add "title"` - Creates task with defaults (priority=medium, category=uncategorized, no due date)
- `todo list` - Shows all tasks with new columns
- `todo update 1 --title "new"` - Still updates only title
- `todo delete 1` - Still deletes task
- `todo complete 1` - Still marks complete
- `todo incomplete 1` - Still marks incomplete

---

## Related Artifacts

- `spec.md`: Feature specification with user stories
- `data-model.md`: Entity definitions and validation rules
- `plan.md`: Implementation plan
- `quickstart.md`: Usage guide
