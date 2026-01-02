---
id: 002
title: Create Implementation Plan Advanced Features
stage: plan
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-advanced-features
branch: 001-advanced-features
user: user
command: /sp.plan
labels: ["plan", "architecture", "recurring-tasks", "reminders", "notifications"]
links:
  spec: specs/001-advanced-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-advanced-features/plan.md
 - specs/001-advanced-features/research.md
 - specs/001-advanced-features/data-model.md
 - specs/001-advanced-features/contracts/cli-api.md
 - specs/001-advanced-features/quickstart.md
 - CLAUDE.md
tests:
 - none
---

## Prompt

Create implementation plan for advanced features (recurring tasks and due date reminders) based on approved specification.

User provided high-level guidance:
1. Recurring Tasks: Modify task creation logic, integrate scheduling system, store recurrence details
2. Due Dates & Time Reminders: Add due date/time fields, implement reminder system, integrate browser notifications
3. High-Level Flow: Add/update tasks with recurrence and due dates, notification handling via scheduler

## Response snapshot

Successfully created implementation plan for "Advanced Features - Recurring Tasks and Due Date Reminders" on branch `001-advanced-features`.

**Planning Artifacts Created**:
1. **plan.md** - Main implementation plan with:
   - Summary of 3 prioritized user stories (P1: due dates/reminders, P2: recurring, P3: combined)
   - Technical context (Python 3.13+, click CLI, standard library, in-memory storage)
   - Constitution check (all gates passed ✓)
   - Project structure (single project, extends existing src/ layout)
   - File-level implementation map

2. **research.md** - Technical research with 6 key decisions:
   - Decision 1: Use `plyer` library for cross-platform desktop notifications
   - Decision 2: Background thread with min-heap (priority queue) for reminder scheduling
   - Decision 3: Composition pattern with RecurrencePattern class
   - Decision 4: Extend Task with `due_time` field (backwards compatible)
   - Decision 5: Single daemon thread polling every 10 seconds
   - Decision 6: Extend existing commands with optional flags (no new commands)

3. **data-model.md** - Detailed entity specifications:
   - Extended Task entity (15 fields including 7 new)
   - RecurrencePattern entity (interval type + value)
   - Reminder entity (internal model for service)
   - ReminderService (background notification thread)
   - RecurrenceService (instance creation logic)
   - Validation rules, methods, state transitions
   - Integration points with existing code

4. **contracts/cli-api.md** - CLI command interface contracts:
   - Extended `todo add` with 4 new flags (--due-time, --recurrence, --recurrence-days, --remind-before)
   - Extended `todo update` with 4 new flags (--no-due, --no-recurrence, --no-reminders, --title)
   - Extended `todo list` with 5 new filters (--overdue, --due-today, --due-this-week, --recurring-only, --sort-by-due)
   - Extended behavior for `todo complete` (auto-creates next recurring instance)
   - Extended behavior for `todo delete` (deletes current instance only)
   - Notification format specification
   - Validation rules and error handling
   - 25+ command examples

5. **quickstart.md** - User guide with:
   - 5 quick start sections (due dates, reminders, recurring, working with recurring, combining features)
   - 4 common use case examples (morning routine, weekly meetings, monthly tasks, project deadlines)
   - Viewing and filtering guidance
   - Updating existing tasks
   - Display format explanation
   - Tips and best practices
   - Troubleshooting section

**Technical Decisions**:
- **Notifications**: plyer library for cross-platform desktop notifications (not browser-based)
- **Scheduling**: Background daemon thread with 10-second polling + priority queue
- **Recurrence Logic**: Composition pattern (RecurrencePattern class) for clean separation
- **Datetime Handling**: Add `due_time` field to Task (backwards compatible with existing `due_date`)
- **Thread Safety**: threading.Lock for shared task store access
- **New Dependencies**: plyer>=2.1.0 (only new external dependency)

**Architecture Highlights**:
- Extends existing Task model (src/models/task.py) with 7 new fields
- Two new model files: recurrence.py, reminder.py
- Two new service files: reminder_service.py, recurrence_service.py
- One new CLI formatter: formatters.py
- No changes to task_store.py (storage agnostic)
- Maintains in-memory storage (per constitution)

**Constitution Compliance**: All gates passed ✓
- Technology stack: Python 3.13+, UV, CLI-only ✓
- Storage: In-memory only (no persistence) ✓
- Features: Implements constitution features #9 and #10 ✓
- Agent workflow: Spec → Plan → Tasks → Implement ✓
- Traceability: Plan references approved spec ✓

**Agent Context Updated**:
- Language: Python 3.13+
- Framework: click (CLI), standard library (datetime, threading)
- Database: In-memory only

## Outcome

- ✅ Impact: Complete implementation plan with research, data model, contracts, and user guide
- 🧪 Tests: Planning artifacts define testable contracts; test strategy included in data-model.md
- 📁 Files: Created 5 planning artifacts (plan.md, research.md, data-model.md, cli-api.md, quickstart.md), updated CLAUDE.md
- 🔁 Next prompts: Ready for `/sp.tasks` to generate implementation tasks from plan and spec
- 🧠 Reflection: Plan successfully balances new features with existing architecture; backwards compatible design; clear separation of concerns (models, services, CLI); all technical unknowns resolved through research

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully
- Graders run and results (PASS/FAIL): Manual validation against constitution - PASS (all gates passed)
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 (research) and Phase 1 (design + contracts)
- Next experiment (smallest change to try): None required - plan is complete and ready for task generation
