# CLI Command Contracts: Todo CLI Application

**Feature**: 001-todo-cli-app
**Created**: 2025-12-30
**Based on**: [spec.md](../001-todo-cli-app/spec.md)

## Command Overview

The application is invoked as `todo` with subcommands for each operation:

```text
todo --help          # Show help
todo add --title "..." [--description "..."]
todo list            # View all tasks
todo update ID [--title "..."] [--description "..."]
todo delete ID
todo complete ID
todo incomplete ID
```

---

## add

Add a new task to the task list.

### Syntax

```text
todo add --title TITLE [--description DESCRIPTION]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--title` | Yes | Task title (1-255 characters) |
| `--description` | No | Task description (0-2000 characters) |

### Output (Success)

```
Added task 1: Buy milk
```

### Output (Error - Empty Title)

```
Error: Task title cannot be empty
```

---

## list

Display all tasks with their status.

### Syntax

```text
todo list
```

### Output (Success - Multiple Tasks)

```
ID | Status      | Title       | Description
---+-------------+-------------+-------------------------
1  | [ ]         | Buy milk    | Get 2% milk from store
2  | [x]         | Call mom    | Wish her happy birthday
3  | [ ]         | Finish report | Q4 sales report
```

### Output (Success - Empty List)

```
No tasks found. Add a task with: todo add --title "Task name"
```

### Output (Legend)

```
Legend: [ ] = Incomplete  [x] = Complete
```

---

## update

Modify an existing task's title and/or description.

### Syntax

```text
todo update ID [--title TITLE] [--description DESCRIPTION]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `ID` | Yes | Task ID to update |
| `--title` | No | New task title (1-255 characters) |
| `--description` | No | New task description (0-2000 characters) |

**Note**: At least one of `--title` or `--description` must be provided.

### Output (Success - Title Update)

```
Updated task 1: Buy almond milk
```

### Output (Success - Description Update)

```
Updated task 1 description
```

### Output (Error - Task Not Found)

```
Error: Task 5 not found
```

### Output (Error - No Changes)

```
Error: No changes provided (use --title and/or --description)
```

---

## delete

Remove a task from the task list.

### Syntax

```text
todo delete ID
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `ID` | Yes | Task ID to delete |

### Output (Success)

```
Deleted task 1
```

### Output (Error - Task Not Found)

```
Error: Task 5 not found
```

---

## complete

Mark a task as complete.

### Syntax

```text
todo complete ID
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `ID` | Yes | Task ID to mark complete |

### Output (Success)

```
Marked task 1 as complete
```

### Output (Error - Task Not Found)

```
Error: Task 5 not found
```

---

## incomplete

Mark a task as incomplete.

### Syntax

```text
todo incomplete ID
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `ID` | Yes | Task ID to mark incomplete |

### Output (Success)

```
Marked task 1 as incomplete
```

### Output (Error - Task Not Found)

```
Error: Task 5 not found
```

---

## Global Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message |
| `--version` | Show version information |

### Help Output

```
Usage: todo [OPTIONS] COMMAND [ARGS]...

A simple CLI todo application for task management.

Options:
  --help  Show this message and exit.

Commands:
  add         Add a new task
  complete    Mark a task as complete
  delete      Delete a task by ID
  incomplete  Mark a task as incomplete
  list        List all tasks
  update      Update a task
```

---

## Error Handling

| Error Condition | Message | Exit Code |
|-----------------|---------|-----------|
| Task not found | `Error: Task {ID} not found` | 1 |
| Invalid ID format | `Error: Invalid ID '{input}'` | 1 |
| Empty title | `Error: Task title cannot be empty` | 1 |
| Title too long | `Error: Title exceeds 255 characters` | 1 |
| Description too long | `Error: Description exceeds 2000 characters` | 1 |
| No changes provided | `Error: No changes provided` | 1 |
| Session data lost | `Error: Session data not available` | 1 |

---

**End of CLI Command Contracts**
