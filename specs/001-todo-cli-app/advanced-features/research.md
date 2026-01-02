# Research: Advanced Features - Recurring Tasks and Due Date Reminders

**Date**: 2026-01-01
**Feature**: 001-advanced-features
**Purpose**: Technical research and decision documentation for implementing recurring tasks and due date reminders in a Python CLI application

## Research Questions

1. How to implement browser notifications from a CLI Python application?
2. What is the best approach for scheduling reminders in-memory without a database?
3. How to handle recurring task logic (interval calculation, instance creation)?
4. How to integrate datetime handling with the existing Task model?
5. What threading/async approach works best for background reminder checking?

---

## Decision 1: Browser Notifications from CLI

**Decision**: Use the `plyer` library for cross-platform desktop notifications

**Rationale**:
- `plyer` provides a unified API for desktop notifications across Windows, macOS, and Linux
- Works natively without requiring a browser to be open
- Simpler than "browser notifications" - these are OS-level desktop notifications
- Fallback to console output if notifications unavailable
- Lightweight with minimal dependencies

**Alternatives Considered**:
- **Browser-based notifications via websocket**: Requires running a web server, violates CLI-only constraint
- **win10toast (Windows only)**: Platform-specific, not cross-platform
- **notify-send (Linux only)**: Platform-specific, requires external binary
- **Console-only alerts**: Misses users when they're not actively watching the terminal

**Implementation Notes**:
- Add `plyer>=2.1.0` to project dependencies
- Desktop notifications will show as system tray/notification center alerts
- Include fallback to console output when plyer is unavailable
- Notifications will only work while the CLI application has a background thread running

---

## Decision 2: In-Memory Reminder Scheduling

**Decision**: Use a background thread with a min-heap (priority queue) to check for due reminders

**Rationale**:
- Python's `threading` module provides lightweight background execution
- `heapq` (priority queue) efficiently tracks next reminder to check
- No external dependencies needed (standard library)
- Integrates well with in-memory storage requirement
- Thread can be started when first task with reminder is added, stopped when app exits

**Alternatives Considered**:
- **APScheduler library**: Overkill for simple interval checking, adds dependency
- **asyncio event loop**: More complex integration with Click CLI, harder to reason about
- **Polling every second**: Inefficient, uses unnecessary CPU when no reminders are near
- **Cron-style scheduling**: Requires persistent scheduler, violates in-memory constraint

**Implementation Notes**:
- Use `threading.Event` for clean shutdown
- Check reminders every 10 seconds (configurable)
- Priority queue ordered by next check time (earliest first)
- Thread-safe access to task storage using locks
- Reminder thread starts automatically when CLI loads tasks with reminders

---

## Decision 3: Recurring Task Logic

**Decision**: Implement recurrence as a composition pattern with a `RecurrencePattern` class

**Rationale**:
- Separation of concerns: Task handles task data, RecurrencePattern handles scheduling logic
- Easy to test recurrence logic independently
- Supports future extension (e.g., skip weekends, monthly on specific day)
- Clear API: `pattern.calculate_next_occurrence(from_date)`
- Follows existing codebase pattern of using dataclasses and enums

**Alternatives Considered**:
- **Embed recurrence fields directly in Task**: Makes Task class too complex, harder to test
- **Use iCalendar RRULE standard**: Overkill for simple daily/weekly/monthly intervals
- **Store recurring tasks separately**: Complicates querying all tasks, violates single responsibility
- **Use external library (python-dateutil.rrule)**: Adds dependency, more complex than needed

**Implementation Notes**:
```python
@dataclass
class RecurrencePattern:
    interval_type: RecurrenceInterval  # DAILY, WEEKLY, MONTHLY, CUSTOM
    interval_value: int = 1  # e.g., 7 for weekly

    def calculate_next_occurrence(self, from_date: datetime) -> datetime:
        # Logic to add interval to from_date
        pass
```

- Task extended with: `recurrence: Optional[RecurrencePattern]`
- On task completion: if recurring, create new instance with next occurrence date
- Preserve all task attributes except completion status and dates

---

## Decision 4: Datetime Handling for Due Dates and Times

**Decision**: Extend Task model with `due_time: Optional[time]` field, combine with existing `due_date: Optional[date]`

**Rationale**:
- Backwards compatible: existing tasks have `due_date` only, new tasks can add `due_time`
- Clear separation: date (YYYY-MM-DD) vs time (HH:MM)
- Easy to display: "Due on 2026-01-10" vs "Due on 2026-01-10 at 17:00"
- Reminder calculation: combine due_date + due_time to get absolute datetime for reminders
- Uses timezone-aware datetimes (UTC) for consistency

**Alternatives Considered**:
- **Single `due_datetime: datetime` field**: Breaking change for existing tasks with due_date
- **Store as string "YYYY-MM-DD HH:MM"**: Requires parsing, error-prone
- **Store as Unix timestamp**: Less readable, harder to display and edit
- **Keep date-only, infer time as 23:59**: Confusing UX, arbitrary default

**Implementation Notes**:
- Add `due_time: Optional[time] = None` to Task dataclass
- Combine `due_date` and `due_time` into full datetime when scheduling reminders
- If `due_time` is None, default to end of day (23:59:59) for backwards compatibility
- Display format: "2026-01-10 17:00" or "2026-01-10" if no time set
- Input format: Accept "YYYY-MM-DD" or "YYYY-MM-DD HH:MM"

---

## Decision 5: Threading Approach for Background Reminders

**Decision**: Single daemon thread that polls reminder queue every 10 seconds

**Rationale**:
- Simple to implement and reason about
- Daemon thread automatically stops when main program exits
- 10-second polling interval provides good balance (requirement: < 30 seconds accuracy)
- Thread-safe with proper locking around shared task storage
- No complex async/await integration needed with Click CLI

**Alternatives Considered**:
- **Asyncio with event loop**: Requires restructuring Click commands, more complexity
- **Multiple threads per reminder**: Resource-intensive, overkill for < 100 reminders
- **Timer threads (threading.Timer)**: Creates many threads, harder to coordinate shutdown
- **No background thread, check on every command**: Misses reminders when user isn't interacting

**Implementation Notes**:
```python
class ReminderService:
    def __init__(self, task_store):
        self.task_store = task_store
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._check_reminders, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join(timeout=1.0)

    def _check_reminders(self):
        while not self.stop_event.is_set():
            # Check for due reminders
            # Send notifications
            # Sleep for 10 seconds
            pass
```

- Start reminder service when CLI initializes
- Stop cleanly on exit (context manager or atexit handler)
- Use `threading.Lock` when accessing task_store from background thread
- Send notifications via plyer in background thread

---

## Decision 6: CLI Command Extensions

**Decision**: Extend existing commands with optional flags rather than creating new commands

**Rationale**:
- Consistent with existing CLI design (--priority, --category flags)
- Reduces command proliferation (no separate `todo add-recurring`, etc.)
- Easier to discover features through `todo add --help`
- Backwards compatible: existing commands work without new flags

**Implementation Notes**:
- `todo add`:
  - Add `--due DATE` (existing, but now also supports TIME)
  - Add `--due-time TIME` (optional, combines with --due)
  - Add `--recurrence [daily|weekly|monthly|custom]`
  - Add `--recurrence-days N` (for custom intervals)
  - Add `--remind-before MINUTES` (can be specified multiple times)

- `todo update`:
  - Support all above flags to modify existing tasks
  - Add `--no-recurrence` to stop recurrence
  - Add `--no-reminders` to clear all reminders

- `todo list`:
  - Add `--overdue` filter
  - Add `--due-today` filter
  - Add `--due-this-week` filter
  - Add `--recurring-only` filter
  - Sort by due date by default (overdue first, then by date/time)

**Example Commands**:
```bash
# Add task with due date and time
todo add "Finish report" --due 2026-01-10 --due-time 17:00 --remind-before 60

# Add recurring task
todo add "Weekly meeting" --recurrence weekly --due 2026-01-03 --due-time 10:00

# Add task with multiple reminders
todo add "Important deadline" --due 2026-01-15 --remind-before 1440 --remind-before 60

# Update task to add recurrence
todo update 5 --recurrence monthly

# List overdue tasks
todo list --overdue
```

---

## Technical Dependencies Summary

### New Dependencies to Add

```toml
[project.dependencies]
plyer = ">=2.1.0"  # Cross-platform desktop notifications
```

### Standard Library Modules

- `threading` - Background reminder checking
- `heapq` - Priority queue for reminder scheduling
- `datetime` - Date/time handling (date, time, datetime, timedelta)
- `time` - Sleep intervals for reminder thread
- `enum` - Recurrence interval types

---

## Risk Assessment

### Technical Risks

1. **Notification delivery timing**
   - Risk: 10-second polling may miss 30-second SLA
   - Mitigation: Use priority queue, wake on nearest reminder, test with margin

2. **Thread safety**
   - Risk: Race conditions between CLI commands and reminder thread
   - Mitigation: Use threading.Lock for all task_store access

3. **Memory usage with many tasks**
   - Risk: 100+ tasks with reminders may consume significant memory
   - Mitigation: Profile with 200+ tasks, optimize data structures if needed

4. **Recurring task proliferation**
   - Risk: Completing recurring tasks creates many instances quickly
   - Mitigation: Document behavior, consider future enhancement to limit instances

### User Experience Risks

1. **Confusion about delete behavior**
   - Risk: Users expect "delete recurring task" to delete all instances
   - Mitigation: Clear CLI output, document behavior in help text

2. **Notification spam**
   - Risk: Multiple reminders for many tasks may overwhelm users
   - Mitigation: Respect OS notification settings, limit to 5 per check

3. **Timezone confusion**
   - Risk: Users may be unclear about timezone handling
   - Mitigation: Always display times in local timezone, document behavior

---

## Decision 7: Interactive Menu Library

**Decision**: Use Click's built-in prompts enhanced with simple helper functions

**Rationale**:
- Click already provides `click.prompt()`, `click.confirm()`, `click.choice()` for basic interactions
- No additional dependencies required (Click already in use)
- Simple and consistent with existing CLI framework
- Sufficient for numbered menu selections and input prompts
- Easy to test and maintain
- Can add `prompt_toolkit` later if advanced features needed (auto-complete, history, etc.)

**Alternatives Considered**:
- **prompt_toolkit library**: Feature-rich (auto-complete, history, syntax highlighting) but adds complexity and dependency
- **PyInquirer**: Nice UI but deprecated, successor (inquirer) has fewer stars and less maintenance
- **questionary**: Modern and clean but adds another dependency
- **Simple input() calls**: Too basic, no validation or formatting helpers

**Implementation Notes**:
```python
# Main menu using Click
def show_main_menu():
    click.echo("\n=== Todo Application ===")
    click.echo("1. Add Task")
    click.echo("2. View Tasks")
    click.echo("3. Update Task")
    click.echo("4. Delete Task")
    click.echo("5. Complete Task")
    click.echo("6. Exit")
    choice = click.prompt("Select an option", type=click.IntRange(1, 6))
    return choice

# Input validation with Click
priority = click.prompt(
    "Priority",
    type=click.Choice(["high", "medium", "low"], case_sensitive=False),
    default="medium"
)
```

---

## Decision 8: Menu Navigation Pattern

**Decision**: Use numbered menu choices (1-9) with clear labels

**Rationale**:
- Numbers are intuitive and universal
- Easy to type (single digit for most menus)
- Clear and unambiguous selection
- Supports 1-9 options per menu (sufficient for main menu)
- Click's `IntRange` type provides built-in validation

**Alternatives Considered**:
- **Letter choices (a-z)**: Less intuitive, users may confuse with text input
- **Arrow key navigation**: Requires prompt_toolkit, more complex, overkill for simple menus
- **Full text commands**: Requires more typing, error-prone
- **Mixed numbers and letters**: Inconsistent, confusing

**Implementation Notes**:
- Main menu: 6 options (1-6)
- Sub-menus (filters, sorts): Keep under 9 options
- Use consistent format: `<number>. <action>`
- Always provide "0. Back to main menu" or "Exit" option
- Clear screen between menu transitions (optional, platform-dependent)

---

## Decision 9: Error Recovery Strategy

**Decision**: Retry up to 3 times with helpful error messages, then return to main menu

**Rationale**:
- 3 attempts is standard UX practice (not too few, not too many)
- Prevents infinite loops from bad input
- Returns to main menu rather than exiting (better UX)
- Error messages explain what went wrong and what format is expected
- Aligns with specification requirement (FR-043)

**Alternatives Considered**:
- **Unlimited retries**: Risk of infinite loops, frustrating for users
- **Single attempt then exit**: Too harsh, forces restart
- **Single attempt then skip field**: May leave tasks in invalid state
- **Back to previous step**: More complex state management, overkill

**Implementation Notes**:
```python
def prompt_with_validation(prompt_text, validator, max_attempts=3):
    for attempt in range(max_attempts):
        value = click.prompt(prompt_text)
        try:
            return validator(value)
        except ValidationError as e:
            click.echo(f"Error: {e}. {max_attempts - attempt - 1} attempts remaining.")
    click.echo("Max attempts reached. Returning to main menu.")
    return None  # Caller checks for None and returns to menu
```

- Validation functions raise `ValidationError` with helpful message
- Error messages include expected format (e.g., "Please use YYYY-MM-DD format")
- Display remaining attempts to set user expectations
- Use colors (click.style) for error messages (red) and success (green)

---

## Decision 10: Keyboard Interrupt Handling

**Decision**: Ctrl+C during prompts returns to main menu; Ctrl+C at main menu prompts for exit confirmation

**Rationale**:
- Standard Unix/CLI behavior (Ctrl+C = interrupt)
- During operation: Assume user wants to cancel current action, not exit entire app
- At main menu: Assume user wants to exit, but confirm to prevent accidental data loss
- Aligns with specification assumption #11

**Alternatives Considered**:
- **Always exit immediately**: Too abrupt, may lose context
- **Always ignore**: Frustrating, no way to cancel
- **Always prompt for exit**: Annoying during multi-step operations

**Implementation Notes**:
```python
def main_menu_loop():
    while True:
        try:
            choice = show_main_menu()
            # Handle choice...
        except KeyboardInterrupt:
            if click.confirm("\nAre you sure you want to exit?", default=False):
                click.echo("Goodbye!")
                break
            # Continue loop if user says no

def add_task_interactive():
    try:
        # Prompt for task details...
        pass
    except KeyboardInterrupt:
        click.echo("\nTask creation cancelled. Returning to main menu.")
        return None
```

- Use try/except KeyboardInterrupt around prompt sections
- Different behavior based on context (main menu vs operation)
- Always clean up and return gracefully (no crashes)

---

## Updated Technical Dependencies

### New Dependencies to Add

```toml
[project.dependencies]
plyer = ">=2.1.0"  # Cross-platform desktop notifications
# Click already included - no additional dependencies for interactive UI
```

### Standard Library Modules

**Existing**:
- `threading` - Background reminder checking
- `heapq` - Priority queue for reminder scheduling
- `datetime` - Date/time handling (date, time, datetime, timedelta)
- `time` - Sleep intervals for reminder thread
- `enum` - Recurrence interval types

**New for Interactive CLI**:
- `os` - Clear screen (os.system('cls' or 'clear'))
- `sys` - Exit codes and signal handling

---

## Updated Risk Assessment

### Technical Risks (Interactive CLI)

1. **Platform-specific terminal behavior**
   - Risk: Colors, clear screen, key handling may differ across OS
   - Mitigation: Test on Windows, macOS, Linux; use Click's cross-platform helpers

2. **Input encoding issues**
   - Risk: Special characters in task titles may cause encoding errors
   - Mitigation: Use UTF-8 encoding; validate/sanitize user input

3. **Terminal width constraints**
   - Risk: Long task titles or menu items may wrap badly
   - Mitigation: Truncate or wrap text intelligently; detect terminal width

### User Experience Risks (Interactive CLI)

1. **Learning curve for keyboard interrupts**
   - Risk: Users may not understand Ctrl+C behavior
   - Mitigation: Display hint in footer (e.g., "Press Ctrl+C to cancel")

2. **Slow menu navigation**
   - Risk: Multiple menu levels may feel tedious
   - Mitigation: Keep menu hierarchy shallow (max 2-3 levels)

---

## Next Steps

Phase 1 (Design & Contracts) will produce:
1. **data-model.md** - Detailed data model for Task, RecurrencePattern, Reminder (update with validation models)
2. **contracts/cli-api.md** - CLI command interface contracts with examples (update with interactive menu flows)
3. **quickstart.md** - User guide for using advanced features (update with interactive examples)
