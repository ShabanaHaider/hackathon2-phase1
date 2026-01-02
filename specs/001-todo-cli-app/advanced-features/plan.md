# Implementation Plan: Advanced Features - Recurring Tasks, Due Date Reminders, and Interactive CLI

**Branch**: `001-advanced-features` | **Date**: 2026-01-01 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-advanced-features/spec.md`
**Updated**: 2026-01-01 (added interactive CLI and input validation)

## Summary

This feature extends the existing in-memory CLI Todo application to support:
1. **Due dates with time-based reminders** (P1): Allow users to set specific due dates/times and receive browser notifications before deadlines
2. **Recurring tasks** (P2): Auto-create new task instances at regular intervals (daily, weekly, monthly, custom)
3. **Combined recurring + reminders** (P3): Support recurring tasks with reminders for each occurrence
4. **Refined interactive CLI interface** (P1): Menu-driven interface with step-by-step prompts and comprehensive input validation

The implementation will extend the existing Task model (src/models/task.py), create interactive menu system in CLI (src/cli/menu.py), add validation layer (src/cli/validation.py), and integrate with existing commands while maintaining in-memory storage as specified by the constitution.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**:
- click (CLI framework)
- plyer (cross-platform desktop notifications)
- standard library (datetime, threading for reminders)
- prompt_toolkit (optional - for enhanced interactive prompts)
**Storage**: In-memory only (per constitution) - no persistence
**Testing**: pytest (existing test infrastructure)
**Target Platform**: CLI application on Windows/Linux/macOS
**Project Type**: Single project (CLI application)
**Performance Goals**:
- Task creation/update < 100ms
- Reminder notification delivery < 30 seconds of scheduled time
- Menu navigation < 1 second response time
- Input validation < 100ms
- Support 100+ concurrent tasks with different schedules
**Constraints**:
- CLI-only interaction (no web/GUI)
- In-memory storage only
- Desktop notifications must work without background services
- Reminders only active while application is running
- Interactive prompts must be intuitive without training
**Scale/Scope**:
- Single-user application
- 100+ tasks with mixed recurrence patterns
- Multiple concurrent reminders
- Interactive menu with 6-10 main actions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constitution Compliance

✅ **Technology Stack**: Python 3.13+, UV, CLI-only, Click framework
✅ **Storage**: In-memory only (no file/database persistence)
✅ **Features**: Implements features #8 (due dates), #9 (recurring), #10 (interactive CLI) from constitution
✅ **Agent Roles**: PlanningAgent creating architectural plan per Agentic Dev Stack workflow
✅ **Traceability**: Plan references approved spec at specs/001-advanced-features/spec.md
✅ **No Manual Coding**: All implementation will follow /sp.tasks → /sp.implement workflow

### Gates Passed

- [x] Features are in constitution scope (features #8, #9, #10)
- [x] Technology stack matches constitution (Python 3.13+, UV, CLI)
- [x] In-memory storage requirement respected
- [x] No GUI/web interfaces introduced
- [x] Agent workflow being followed (spec → plan → tasks → implement)
- [x] Interactive CLI aligns with feature #10 "Refined interactive CLI interface"

**Result**: All gates passed ✓

## Project Structure

### Documentation (this feature)

```text
specs/001-advanced-features/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (updated with interactive CLI)
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Spec quality checklist
├── research.md          # Phase 0 output (already exists)
├── data-model.md        # Phase 1 output (needs update for validation)
├── quickstart.md        # Phase 1 output (needs update for interactive mode)
├── contracts/           # Phase 1 output (needs update for menu)
│   └── cli-api.md       # CLI command interface contracts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── task.py                 # Extended with due_time, recurrence, reminders
│   ├── recurrence.py           # NEW: Recurrence pattern logic
│   └── reminder.py             # NEW: Reminder scheduling and notification
├── services/
│   ├── reminder_service.py     # NEW: Background reminder checking
│   └── recurrence_service.py   # NEW: Recurring task instance creation
├── cli/
│   ├── commands.py             # Extended with due date, recurrence, reminder options
│   ├── menu.py                 # NEW: Interactive menu system
│   ├── prompts.py              # NEW: User prompt handlers
│   ├── validation.py           # NEW: Input validation layer
│   └── formatters.py           # NEW: Display formatting for dates and recurrence
└── storage/
    └── task_store.py           # Existing in-memory storage (no changes needed)

tests/
├── unit/
│   ├── test_task.py            # Extended with recurrence and reminder tests
│   ├── test_recurrence.py      # NEW: Recurrence logic tests
│   ├── test_reminder.py        # NEW: Reminder scheduling tests
│   ├── test_validation.py      # NEW: Input validation tests
│   └── test_menu.py            # NEW: Menu navigation tests
└── integration/
    └── test_cli_advanced.py    # NEW: End-to-end tests for advanced features
```

**Structure Decision**: Single project structure (Option 1) is appropriate since this is a CLI application. The existing src/models/, src/cli/, and src/storage/ structure will be extended with new modules for recurrence, reminder logic, interactive menu system, and validation.

## Complexity Tracking

> No constitution violations detected. All requirements align with constitution scope and constraints.

## Updates Required for Interactive CLI

The existing planning artifacts (research.md, data-model.md, contracts/cli-api.md, quickstart.md) were created before the interactive CLI feature was added to the specification. They focus on command-line flags rather than interactive prompts. The following updates are needed:

### Research.md Updates Needed
- Decision on interactive menu library (use Click's built-in prompts vs prompt_toolkit)
- Decision on menu navigation pattern (numbered choices vs lettered choices)
- Decision on error recovery strategy (retry limits, back/cancel options)

### Data-Model.md Updates Needed
- No changes to Task, RecurrencePattern, or Reminder entities
- Add validation models/rules for each input type
- Document menu state management (if needed)

### Contracts/cli-api.md Updates Needed
- Add interactive menu flow specifications
- Document prompt sequences for each operation
- Specify validation error messages and formats
- Define menu navigation paths

### Quickstart.md Updates Needed
- Replace command-line flag examples with interactive menu examples
- Add screenshots or ASCII art of menu interfaces
- Document how to navigate the interactive system
- Provide troubleshooting for interactive mode

**Next Steps**: Proceed with Phase 0 (research updates) and Phase 1 (update existing artifacts + create validation specs)
