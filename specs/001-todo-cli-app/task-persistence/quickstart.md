# Quickstart: Task Management CLI Enhancements

**Feature**: Task Management CLI Enhancements
**Created**: 2026-01-01

This guide covers the new features for managing task priority, category, due dates, filtering, and sorting.

## Getting Started

### Prerequisites

- Python 3.13+
- UV package manager
- Todo CLI installed

### Installation

```bash
# Clone and setup
git clone <repository>
cd hack2todo
uv pip install -e .
```

## Adding Tasks with Attributes

### Basic Task

```bash
todo add "Buy milk"
```

Creates a task with default values:
- Priority: medium
- Category: uncategorized
- Due date: none

### Task with Priority

```bash
todo add "Finish report" --priority high
todo add "Weekend project" --priority low
```

Priority options: `high`, `medium`, `low`

### Task with Category

```bash
todo add "Team meeting" --category work
todo add "Grocery shopping" --category home
```

Category options: `work`, `home`

### Task with Due Date

```bash
todo add "Submit proposal" --due-date 2026-01-15
```

Date format: YYYY-MM-DD

### Full Task Example

```bash
todo add "Q1 review" \
    --priority high \
    --category work \
    --due-date 2026-01-20 \
    --description "Review quarterly performance metrics"
```

## Viewing Tasks

### List All Tasks

```bash
todo list
```

Output includes all task attributes:
```
ID  | Status    | Title          | Priority | Category | Due Date
----|-----------|----------------|----------|----------|------------
1   | [ ]       | Buy milk       | medium   | home     |
2   | [ ]       | Finish report  | high     | work     | 2026-01-20
```

### Filter by Status

```bash
# Show only pending tasks
todo list --status pending

# Show only completed tasks
todo list --status completed
```

### Filter by Priority

```bash
# Show only high priority tasks
todo list --priority high

# Show medium priority tasks
todo list --priority medium

# Show low priority tasks
todo list --priority low
```

### Filter by Category

```bash
# Show only work tasks
todo list --category work

# Show only home tasks
todo list --category home
```

### Combine Filters

```bash
# High priority work tasks
todo list --priority high --category work
```

### Sort Tasks

```bash
# Sort by due date
todo list --sort-by due_date

# Sort by priority (high -> medium -> low)
todo list --sort-by priority

# Sort alphabetically by title
todo list --sort-by title

# Reverse sort order
todo list --sort-by title --sort-order desc
```

## Updating Tasks

### Update Priority

```bash
todo update 1 --priority high
```

### Update Category

```bash
todo update 1 --category work
```

### Update Due Date

```bash
# Set a due date
todo update 1 --due-date 2026-02-01

# Clear the due date
todo update 1 --due-date ""
```

### Update Multiple Attributes

```bash
todo update 1 \
    --priority high \
    --category work \
    --due-date 2026-01-25
```

## Managing Task Status

### Complete a Task

```bash
todo complete 1
```

### Mark Incomplete

```bash
todo incomplete 1
```

## Deleting Tasks

```bash
todo delete 1
```

## Complete Workflow Example

```bash
# Day 1: Add tasks for the week
todo add "Team standup" --priority high --category work --due-date 2026-01-06
todo add "Submit timesheet" --priority high --category work --due-date 2026-01-05
todo add "Buy groceries" --priority medium --category home --due-date 2026-01-04
todo add "Plan weekend trip" --priority low --category home --due-date 2026-01-10

# See what needs attention
todo list --status pending --sort-by due_date

# Mark high priority items complete
todo complete 1
todo complete 2

# Check work tasks
todo list --category work

# Day 2: Update priorities as things change
todo update 3 --priority high
todo update 4 --due-date 2026-01-08
```

## Tips

1. **Use priority levels**: High for urgent tasks, medium for normal tasks, low for when-you-can tasks
2. **Set due dates**: Helps visualize upcoming deadlines
3. **Categorize tasks**: Separate work and personal tasks for clarity
4. **Combine filters**: Use multiple filters to focus on specific task groups
5. **Sort strategically**: Due date sorting helps identify upcoming deadlines

## Troubleshooting

### "Invalid priority. Must be high, medium, or low."

Priority values are case-insensitive but must be one of the three options.

### "Invalid date format. Use YYYY-MM-DD."

Ensure the date is in the format: YYYY-MM-DD (e.g., 2026-01-15)

### "Task not found."

The task ID may have been deleted or doesn't exist. Run `todo list` to see available tasks.

### Tasks not showing new columns

Ensure you're using the latest version of the CLI. Reinstall with `uv pip install -e .`

## Related Commands

| Command | Description |
|---------|-------------|
| `todo add "title"` | Add a new task |
| `todo list` | List all tasks |
| `todo update <id>` | Update a task |
| `todo delete <id>` | Delete a task |
| `todo complete <id>` | Mark task complete |
| `todo incomplete <id>` | Mark task incomplete |
