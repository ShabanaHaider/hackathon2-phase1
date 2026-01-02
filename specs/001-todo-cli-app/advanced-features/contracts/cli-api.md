# CLI API Contracts: Advanced Features

**Date**: 2026-01-01
**Feature**: 001-advanced-features
**Purpose**: Command-line interface contracts for recurring tasks and due date reminders

---

## Command: `todo add` (Extended)

**Purpose**: Create a new task with optional due date/time, recurrence, and reminders

### Syntax

```bash
todo add TITLE [OPTIONS]
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `TITLE` | string | Yes | Task title (max 255 chars) |

### Options (Existing)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--description TEXT` | string | `""` | Detailed task description |
| `--priority [high\|medium\|low]` | choice | `medium` | Task priority |
| `--category [work\|home\|uncategorized]` | choice | `uncategorized` | Task category |
| `--due DATE` | string | None | Due date (YYYY-MM-DD format) |

### Options (New)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--due-time TIME` | string | None | Due time (HH:MM format, requires --due) |
| `--recurrence [daily\|weekly\|monthly\|custom]` | choice | None | Make task recurring |
| `--recurrence-days N` | integer | None | Days for custom recurrence (requires --recurrence custom) |
| `--remind-before MINUTES` | integer | None | Reminder before due time (can be used multiple times, max 5) |

### Examples

**Basic task with due date and time**:
```bash
todo add "Finish report" --due 2026-01-10 --due-time 17:00
```

**Task with reminder**:
```bash
todo add "Meeting with client" --due 2026-01-05 --due-time 14:00 --remind-before 15
```

**Task with multiple reminders**:
```bash
todo add "Project deadline" --due 2026-01-15 --due-time 23:59 --remind-before 1440 --remind-before 60
# Reminds 1 day before and 1 hour before
```

**Daily recurring task**:
```bash
todo add "Daily standup" --due 2026-01-02 --due-time 09:00 --recurrence daily
```

**Weekly recurring task**:
```bash
todo add "Team meeting" --due 2026-01-03 --due-time 10:00 --recurrence weekly
```

**Monthly recurring task**:
```bash
todo add "Monthly report" --due 2026-01-31 --due-time 17:00 --recurrence monthly
```

**Custom recurring task (every 3 days)**:
```bash
todo add "Water plants" --recurrence custom --recurrence-days 3
```

**Complex recurring task with reminders**:
```bash
todo add "Submit timesheet" --due 2026-01-05 --due-time 17:00 --recurrence weekly --remind-before 60 --remind-before 15
# Every Friday at 5 PM, remind at 4 PM and 4:45 PM
```

### Validation Rules

1. `--due-time` requires `--due` to be set
2. `--recurrence-days` requires `--recurrence custom`
3. `--remind-before` requires `--due` to be set
4. Maximum 5 `--remind-before` values per task
5. `--remind-before` values must be positive integers
6. Title cannot be empty and must be ≤ 255 characters

### Success Output

```
✓ Task created successfully
  ID: 15
  Title: "Meeting with client"
  Due: 2026-01-05 14:00
  Reminder: 15 minutes before (13:45)
```

### Error Examples

```bash
# Error: due-time without due date
$ todo add "Task" --due-time 10:00
Error: --due-time requires --due to be set

# Error: recurrence-days without custom
$ todo add "Task" --recurrence-days 5
Error: --recurrence-days requires --recurrence custom

# Error: remind-before without due date
$ todo add "Task" --remind-before 15
Error: --remind-before requires --due to be set

# Error: too many reminders
$ todo add "Task" --due 2026-01-10 --remind-before 1 --remind-before 2 --remind-before 3 --remind-before 4 --remind-before 5 --remind-before 6
Error: Maximum 5 reminders per task
```

---

## Command: `todo update` (Extended)

**Purpose**: Update an existing task's properties, including due date/time, recurrence, and reminders

### Syntax

```bash
todo update TASK_ID [OPTIONS]
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `TASK_ID` | integer | Yes | ID of the task to update |

### Options (Existing + New)

All options from `todo add` plus:

| Option | Type | Description |
|--------|------|-------------|
| `--no-due` | flag | Remove due date and time |
| `--no-recurrence` | flag | Stop task from recurring |
| `--no-reminders` | flag | Clear all reminders |
| `--title TEXT` | string | Update task title |

### Examples

**Add due date to existing task**:
```bash
todo update 5 --due 2026-01-10 --due-time 15:00
```

**Make existing task recurring**:
```bash
todo update 8 --recurrence weekly
```

**Add reminders to existing task**:
```bash
todo update 3 --remind-before 60 --remind-before 15
```

**Remove recurrence from task**:
```bash
todo update 12 --no-recurrence
```

**Remove all reminders**:
```bash
todo update 7 --no-reminders
```

**Change recurrence pattern**:
```bash
todo update 9 --recurrence monthly
# Changes from weekly to monthly
```

**Update due time only** (keeps due date):
```bash
todo update 4 --due-time 18:00
```

### Success Output

```
✓ Task updated successfully
  ID: 5
  Title: "Project deadline"
  Due: 2026-01-10 15:00
  Recurrence: None
  Reminders: None
```

### Error Examples

```bash
# Error: Task not found
$ todo update 999 --due 2026-01-10
Error: Task with ID 999 not found

# Error: Invalid due time format
$ todo update 5 --due-time 25:00
Error: Invalid time format. Use HH:MM (00:00 to 23:59)
```

---

## Command: `todo list` (Extended)

**Purpose**: Display tasks with filtering and sorting options for due dates and recurrence

### Syntax

```bash
todo list [OPTIONS]
```

### Options (Existing)

| Option | Type | Description |
|--------|------|-------------|
| `--priority [high\|medium\|low]` | choice | Filter by priority |
| `--category [work\|home\|uncategorized]` | choice | Filter by category |
| `--status [complete\|incomplete]` | choice | Filter by status |

### Options (New)

| Option | Type | Description |
|--------|------|-------------|
| `--overdue` | flag | Show only overdue tasks |
| `--due-today` | flag | Show only tasks due today |
| `--due-this-week` | flag | Show only tasks due within 7 days |
| `--recurring-only` | flag | Show only recurring tasks |
| `--sort-by-due` | flag | Sort by due date (overdue first, then ascending) |

### Display Format (Extended)

```
ID │ Title                │ Status │ Priority │ Category │ Due Date       │ Recurs │ Reminders
───┼─────────────────────┼────────┼──────────┼──────────┼────────────────┼────────┼──────────
 1 │ Finish report        │ ☐      │ high     │ work     │ 2026-01-10 17:00 │ -      │ 1h before
 2 │ [OVERDUE] Pay bills  │ ☐      │ high     │ home     │ 2025-12-31 23:59 │ -      │ -
 3 │ Weekly meeting       │ ☐      │ medium   │ work     │ 2026-01-03 10:00 │ Weekly │ 15m before
 4 │ Daily standup        │ ☐      │ low      │ work     │ 2026-01-02 09:00 │ Daily  │ -
 5 │ Buy groceries        │ ☐      │ medium   │ home     │ -                │ -      │ -
```

### Examples

**Show all overdue tasks**:
```bash
todo list --overdue
```

**Show tasks due today**:
```bash
todo list --due-today
```

**Show tasks due this week**:
```bash
todo list --due-this-week
```

**Show only recurring tasks**:
```bash
todo list --recurring-only
```

**Sort all tasks by due date**:
```bash
todo list --sort-by-due
```

**Combine filters**:
```bash
todo list --status incomplete --priority high --due-this-week --sort-by-due
```

### Legend

- `☐` = Incomplete
- `☑` = Complete
- `[OVERDUE]` = Past due date/time and not complete
- `Recurs` column: Daily, Weekly, Monthly, or days count (e.g., "3d" for every 3 days)
- `Reminders` column: First reminder interval (e.g., "1h before", "15m before")

---

## Command: `todo complete` (Extended Behavior)

**Purpose**: Mark a task as complete (creates next instance if recurring)

### Syntax

```bash
todo complete TASK_ID
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `TASK_ID` | integer | Yes | ID of the task to mark complete |

### Behavior Changes

**Non-recurring task**: Same as before - marks complete

**Recurring task**:
1. Marks current task complete
2. Creates new task instance with next occurrence date
3. Shows information about the next instance

### Examples

**Complete non-recurring task**:
```bash
$ todo complete 5
✓ Task marked as complete
  ID: 5
  Title: "Finish report"
```

**Complete recurring task**:
```bash
$ todo complete 8
✓ Task marked as complete
  ID: 8
  Title: "Weekly meeting"

↻ Next instance created
  ID: 15
  Title: "Weekly meeting"
  Due: 2026-01-10 10:00 (in 7 days)
  Recurrence: Weekly
  Reminders: 15 minutes before
```

---

## Command: `todo delete` (Recurring Task Behavior)

**Purpose**: Delete a task (for recurring tasks, deletes only current instance)

### Syntax

```bash
todo delete TASK_ID
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `TASK_ID` | integer | Yes | ID of the task to delete |

### Behavior

**Non-recurring task**: Deletes the task permanently

**Recurring task**:
1. Deletes only the current instance
2. Future instances (if already created) remain intact
3. Shows confirmation message

### Examples

**Delete non-recurring task**:
```bash
$ todo delete 5
✓ Task deleted
  ID: 5
  Title: "Finish report"
```

**Delete recurring task instance**:
```bash
$ todo delete 8
✓ Current instance deleted
  ID: 8
  Title: "Weekly meeting"

Note: This is a recurring task. Only this instance was deleted.
      Future instances remain scheduled.
```

---

## Notification Format

**Desktop Notification** (via plyer):

```
─────────────────────────
  Todo Reminder
─────────────────────────
Task: "Meeting with client"
Due: 2026-01-05 14:00
Time remaining: 15 minutes
─────────────────────────
```

**Console Fallback** (if desktop notifications unavailable):

```
[REMINDER] Meeting with client (due in 15 minutes at 14:00)
```

---

## Validation Summary

### Input Validation

1. **Date format**: YYYY-MM-DD (validates with datetime.date.fromisoformat)
2. **Time format**: HH:MM (validates with datetime.time.fromisoformat)
3. **Reminder intervals**: Positive integers only
4. **Recurrence days**: Positive integers only (for custom recurrence)
5. **Task ID**: Must be valid integer and exist in storage

### Cross-Field Validation

1. `due_time` requires `due_date`
2. `remind_before` requires `due_date`
3. `recurrence_days` requires `recurrence=custom`
4. Maximum 5 reminders per task

### Error Handling

- Invalid format → Clear error message with expected format
- Missing required field → Error with which field is missing
- Task not found → Error with task ID
- Validation failure → Error with validation rule violated

---

## Integration Points

### With ReminderService

- After creating/updating task with reminders → call `refresh_reminders()`
- After completing/deleting task → call `refresh_reminders()`
- ReminderService polls every 10 seconds and sends notifications

### With RecurrenceService

- After marking recurring task complete → call `create_next_instance()`
- New instance inherits all attributes except status and dates
- Display message showing next instance details

### With TaskStore

- All commands use existing TaskStore methods (add, update, delete, get_all)
- No schema changes needed - Task model handles serialization

---

## Summary

The CLI API extends existing commands with minimal breaking changes:
- `todo add` gains new optional flags for due time, recurrence, and reminders
- `todo update` supports all new fields plus negation flags (--no-*)
- `todo list` gains filtering and sorting for date-based queries
- `todo complete` and `todo delete` have special behavior for recurring tasks

All new features are opt-in through flags, maintaining backwards compatibility with existing workflows.
