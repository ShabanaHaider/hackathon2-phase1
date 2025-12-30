# Tasks: Todo CLI Application

**Feature Branch**: `001-todo-cli-app`
**Generated**: 2025-12-30
**Specification**: [specs/001-todo-cli-app/spec.md](../001-todo-cli-app/spec.md)
**Plan**: [specs/001-todo-cli-app/plan.md](../001-todo-cli-app/plan.md)

## Overview

This task list breaks down the Todo CLI application implementation into atomic, traceable tasks organized by user story. Each task is designed to be independently executable by an AI agent.

## User Story Mapping

| User Story | Priority | Description | Tasks |
|------------|----------|-------------|-------|
| US1 | P1 | Add and View Tasks | T004-T007 |
| US2 | P2 | Update and Delete Tasks | T008-T010 |
| US3 | P2 | Mark Complete/Incomplete | T011-T013 |

## Phase 1: Project Setup

Initialize the project structure with UV, Python 3.13+, and required dependencies.

### Story Goal

Establish development environment and project structure.

### Independent Test Criteria

- `uv run python --version` returns Python 3.13+
- `pyproject.toml` exists with click and pytest dependencies
- Directory structure matches plan.md specification

### Implementation Tasks

- [x] T001 Create pyproject.toml with Python 3.13+, UV configuration, click, pytest
- [x] T002 Create src/__init__.py to make src a package
- [x] T003 Create tests/__init__.py to make tests a package

---

## Phase 2: Foundational (Models & Storage)

Create the core data model and in-memory storage layer. These tasks are prerequisites for all user stories.

### Story Goal

Implement the Task entity and TaskStore that all features depend on.

### Independent Test Criteria

- `Task` dataclass can be instantiated with required fields
- `TaskStore` can add, retrieve, list, update, delete, and mark tasks complete/incomplete
- All CRUD operations maintain data integrity

### Implementation Tasks

- [x] T004 [US1] Create Task model in src/models/task.py with dataclass
- [x] T005 [US1] Create TaskStore in src/storage/task_store.py with in-memory storage
- [x] T006 [US1] Create tests/unit/test_task.py for Task model tests
- [x] T007 [US1] Create tests/unit/test_task_store.py for TaskStore tests

---

## Phase 3: User Story 1 - Add and View Tasks

Implement add and list commands for basic task management.

### Story Goal

Users can add tasks with title/description and view all tasks with completion status.

### Independent Test Criteria

- `todo add --title "Buy milk"` creates a task and outputs "Added task 1: Buy milk"
- `todo list` displays all tasks with ID, status ([ ]/[x]), title, description
- Empty list shows "No tasks found" message

### Acceptance Scenarios

1. Add task with title and description
2. Add task with title only
3. View all tasks (single, multiple, empty)
4. Error on empty title

### Implementation Tasks

- [x] T008 [US1] Create src/cli/__init__.py for CLI module
- [x] T009 [US1] Create src/cli/commands.py with click group and add command
- [x] T010 [US1] Create src/cli/commands.py with list command
- [x] T011 [US1] Update pyproject.toml to configure todo as console script entry point
- [x] T012 [US1] Run pytest tests/unit/ and verify all tests pass

---

## Phase 4: User Story 2 - Update and Delete Tasks

Implement update and delete commands for task maintenance.

### Story Goal

Users can modify task details and remove unwanted tasks.

### Independent Test Criteria

- `todo update 1 --title "New title"` updates task 1's title
- `todo update 1 --description "New desc"` updates task 1's description
- `todo delete 1` removes task 1 and subsequent list no longer shows it
- Invalid task ID shows appropriate error message

### Acceptance Scenarios

1. Update task title
2. Update task description
3. Delete task by ID
4. Error on non-existent task ID

### Implementation Tasks

- [x] T013 [US2] Add update command to src/cli/commands.py with --title and --description options
- [x] T014 [US2] Add delete command to src/cli/commands.py
- [x] T015 [US2] Run pytest tests/unit/ and verify all tests pass

---

## Phase 5: User Story 3 - Mark Complete/Incomplete

Implement commands to toggle task completion status.

### Story Goal

Users can mark tasks as complete or incomplete to track progress.

### Independent Test Criteria

- `todo complete 1` marks task 1 as complete and outputs "Marked task 1 as complete"
- `todo incomplete 1` marks task 1 as incomplete and outputs "Marked task 1 as incomplete"
- Completed tasks display as `[x]` in list output
- Invalid task ID shows appropriate error message

### Acceptance Scenarios

1. Mark task complete
2. Mark task incomplete
3. View reflects status change correctly
4. Error on non-existent task ID

### Implementation Tasks

- [x] T016 [US3] Add complete command to src/cli/commands.py
- [x] T017 [US3] Add incomplete command to src/cli/commands.py
- [x] T018 [US3] Run pytest tests/unit/ and verify all tests pass

---

## Phase 6: Polish & Cross-Cutting Concerns

Final touches, documentation, and integration verification.

### Story Goal

Ensure complete, polished deliverable with documentation and integration testing.

### Independent Test Criteria

- `todo --help` displays all commands
- `todo --version` shows version information
- README.md documents all commands with examples
- All acceptance scenarios from spec.md pass

### Implementation Tasks

- [x] T019 Add --help and --version options to CLI
- [x] T020 Create README.md with command documentation and examples
- [x] T021 Run full integration test: add, list, update, complete, list, delete, list
- [x] T022 Run pytest tests/ --tb=short and verify all tests pass

---

## Dependency Graph

```
Phase 1 (T001-T003)
      ↓
Phase 2 (T004-T007)
      ↓
Phase 3 (T008-T012) ── US1 Complete
      ↓
Phase 4 (T013-T015) ── US2 Complete
      ↓
Phase 5 (T016-T018) ── US3 Complete
      ↓
Phase 6 (T019-T022)
      ↓
END
```

## Parallel Execution Opportunities

| Tasks | Can Run In Parallel Because |
|-------|----------------------------|
| T004, T005 | Different files (models/task.py, storage/task_store.py) |
| T006, T007 | Different files (separate test modules) |
| T009, T010 | Different commands in same file (no file conflict) |
| T013, T014 | Different commands in same file (no file conflict) |
| T016, T017 | Different commands in same file (no file conflict) |

## Implementation Strategy

**MVP First (T001-T012)**:
- Phase 1 + Phase 2 + Phase 3 delivers basic add/list functionality
- Users can add tasks and view them
- Demonstrates core value proposition

**Incremental Delivery**:
- Add update/delete after MVP (Phase 4)
- Add mark complete/incomplete after (Phase 5)
- Polish and document last (Phase 6)

## Task Summary

| Phase | User Story | Tasks | Description |
|-------|------------|-------|-------------|
| 1 | - | T001-T003 | Project Setup |
| 2 | US1 | T004-T007 | Models & Storage |
| 3 | US1 | T008-T012 | Add & List Commands |
| 4 | US2 | T013-T015 | Update & Delete Commands |
| 5 | US3 | T016-T018 | Complete/Incomplete Commands |
| 6 | - | T019-T022 | Polish & Documentation |
| **Total** | - | **22 Tasks** | |

---

**Next Command**: `/sp.implement` to execute tasks

**Task Execution Order**: Execute sequentially (T001 → T022). Tasks marked [P] can run in parallel with other [P] tasks in the same phase if desired.
