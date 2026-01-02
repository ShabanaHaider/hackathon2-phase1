# Tasks: Task Management CLI Enhancements

**Input**: Design documents from `specs/003-task-persistence/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/cli-commands.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project is already set up - verify existing structure is adequate

**Note**: Project structure verified in plan.md - existing structure supports the new feature

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model infrastructure that MUST be complete before any user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Enums

- [X] T001 [P] Create TaskPriority enum in src/models/task.py (HIGH, MEDIUM, LOW)
- [X] T002 [P] Create TaskCategory enum in src/models/task.py (WORK, HOME, UNCATEGORIZED)

### Task Model Updates

- [X] T003 Update Task dataclass to include priority, category, due_date fields in src/models/task.py
- [X] T004 Add __post_init__ validation for new fields in src/models/task.py
- [X] T005 Add update_priority() method in src/models/task.py
- [X] T006 Add update_category() method in src/models/task.py
- [X] T007 Add update_due_date() method in src/models/task.py
- [X] T008 Update to_dict() to include new fields in src/models/task.py
- [X] T009 Update from_dict() to handle new fields with defaults in src/models/task.py

### TaskStore Foundation

- [X] T010 Update TaskStore.add() to accept priority, category, due_date in src/storage/task_store.py
- [X] T011 Update TaskStore.update() to accept priority, category, due_date in src/storage/task_store.py

**Checkpoint**: Foundation ready - data model and storage support new attributes

---

## Phase 3: User Story 1 - Add Tasks with Attributes (Priority: P1) MVP

**Goal**: Users can add tasks with priority, category, and due date attributes

**Independent Test**: Run `todo add "Buy milk" --priority high --category home --due-date 2026-01-15` - task should be created with all attributes

### CLI Command Updates

- [X] T012 [P] [US1] Add --priority option to add command in src/cli/commands.py
- [X] T013 [P] [US1] Add --category option to add command in src/cli/commands.py
- [X] T014 [P] [US1] Add --due-date option to add command in src/cli/commands.py
- [X] T015 [US1] Update add command handler to parse and pass attributes to TaskStore.add() in src/cli/commands.py
- [X] T016 [US1] Add date validation for --due-date input (YYYY-MM-DD format) in src/cli/commands.py

### Validation Tests

- [X] T017 [US1] Test task creation with valid priority, category, and due date
- [X] T018 [US1] Test task creation with default values (no optional attributes)
- [X] T019 [US1] Test invalid priority value shows error message
- [X] T020 [US1] Test invalid category value shows error message
- [X] T021 [US1] Test invalid date format shows error message

**Checkpoint**: User Story 1 validated - tasks can be created with all attributes

---

## Phase 4: User Story 2 - Update Task Attributes (Priority: P1)

**Goal**: Users can update priority, category, and due date of existing tasks

**Independent Test**: Run `todo update 1 --priority high --category work --due-date 2026-01-20` - task attributes should be updated

### CLI Command Updates

- [X] T022 [P] [US2] Add --priority option to update command in src/cli/commands.py
- [X] T023 [P] [US2] Add --category option to update command in src/cli/commands.py
- [X] T024 [P] [US2] Add --due-date option to update command in src/cli/commands.py
- [X] T025 [US2] Update update command handler to parse and pass attributes to TaskStore.update() in src/cli/commands.py
- [X] T026 [US2] Add logic to clear due date when empty string is provided in src/cli/commands.py

### Update Tests

- [X] T027 [US2] Test updating priority only
- [X] T028 [US2] Test updating category only
- [X] T029 [US2] Test updating due date only
- [X] T030 [US2] Test clearing due date with empty string
- [X] T031 [US2] Test updating multiple attributes at once

**Checkpoint**: User Story 2 validated - task attributes can be updated

---

## Phase 5: User Story 3 - Filter Tasks (Priority: P2)

**Goal**: Users can filter tasks by status, priority, and category

**Independent Test**: Run `todo list --priority high --category work` - only matching tasks should be displayed

### TaskStore Filtering

- [X] T032 [P] [US3] Create TaskFilter dataclass in src/storage/task_store.py
- [X] T033 [P] [US3] Implement TaskStore.filter() method with status, priority, category criteria in src/storage/task_store.py
- [X] T034 [US3] Support filtering by multiple criteria simultaneously in src/storage/task_store.py

### CLI Filtering Options

- [X] T035 [P] [US3] Add --status filter option to list command in src/cli/commands.py
- [X] T036 [P] [US3] Add --priority filter option to list command in src/cli/commands.py
- [X] T037 [P] [US3] Add --category filter option to list command in src/cli/commands.py
- [X] T038 [US3] Update list command handler to call TaskStore.filter() with criteria in src/cli/commands.py

### Filtering Tests

- [X] T039 [US3] Test filtering by status (pending/completed)
- [X] T040 [US3] Test filtering by priority (high/medium/low)
- [X] T041 [US3] Test filtering by category (work/home)
- [X] T042 [US3] Test combining multiple filters
- [X] T043 [US3] Test filtering when no tasks match

**Checkpoint**: User Story 3 validated - tasks can be filtered by multiple criteria

---

## Phase 6: User Story 4 - Sort Tasks (Priority: P2)

**Goal**: Users can sort tasks by due date, priority, or title

**Independent Test**: Run `todo list --sort-by priority` - tasks should appear in priority order (high > medium > low)

### TaskStore Sorting

- [X] T044 [P] [US4] Create TaskSort dataclass in src/storage/task_store.py
- [X] T045 [P] [US4] Implement TaskStore.sort() method with due_date, priority, title options in src/storage/task_store.py
- [X] T046 [US4] Handle null due dates (sort to end) in src/storage/task_store.py

### CLI Sorting Options

- [X] T047 [P] [US4] Add --sort-by option to list command in src/cli/commands.py
- [X] T048 [P] [US4] Add --sort-order option (asc/desc) to list command in src/cli/commands.py
- [X] T049 [US4] Update list command handler to call TaskStore.sort() in src/cli/commands.py

### Sorting Tests

- [X] T050 [US4] Test sorting by due date (earliest first)
- [X] T051 [US4] Test sorting by priority (high > medium > low)
- [X] T052 [US4] Test sorting by title (alphabetical)
- [X] T053 [US4] Test reverse sort order
- [X] T054 [US4] Test sorting with null due dates

**Checkpoint**: User Story 4 validated - tasks can be sorted by multiple criteria

---

## Phase 7: User Story 5 - View Task Details (Priority: P2)

**Goal**: All task attributes are visible in the list output

**Independent Test**: Run `todo list` - display should include priority, category, and due date columns

### List Display Updates

- [X] T055 [US5] Update list command to display priority column in src/cli/commands.py
- [X] T056 [US5] Update list command to display category column in src/cli/commands.py
- [X] T057 [US5] Update list command to display due date column in src/cli/commands.py
- [X] T058 [US5] Handle null due date display (show "-" or "None") in src/cli/commands.py

### Display Tests

- [X] T059 [US5] Test list output shows all task attributes
- [X] T060 [US5] Test list output format is readable
- [X] T061 [US5] Test null due date displays correctly

**Checkpoint**: User Story 5 validated - all attributes visible in list output

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Backward compatibility, edge cases, and integration testing

### Backward Compatibility

- [X] T062 Verify existing commands without new options still work correctly
- [X] T063 Verify legacy tasks (without new fields) load with defaults

### Edge Cases

- [X] T064 Handle past due dates (no restriction, but display clearly)
- [X] T065 Handle case-insensitive priority and category inputs
- [X] T066 Handle invalid date values (e.g., 2026-02-30)

### Integration Tests

- [X] T067 Full workflow test: add, update, filter, sort, list
- [X] T068 Test persistence of new attributes across CLI invocations

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - skipped
- **Foundational (Phase 2)**: No dependencies - can start immediately
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - foundation for all other stories
- **User Story 2 (P1)**: Depends on Foundational (Phase 2) - independent of US1
- **User Story 3 (P2)**: Depends on Foundational (Phase 2) - independent of US1, US2
- **User Story 4 (P2)**: Depends on Foundational (Phase 2) - independent
- **User Story 5 (P2)**: Depends on Foundational (Phase 2) - independent

### Within Each User Story

- Foundational must complete before any story can be implemented
- Tasks marked [P] within a story can run in parallel
- Each story is independently testable after implementation

### Parallel Opportunities

- T001-T009: Enum, model, and store foundation tasks (mostly independent)
- T012-T016: CLI add command options (can parallelize)
- T022-T026: CLI update command options (can parallelize)
- T032-T034: TaskStore filter implementation (can parallelize)
- T044-T046: TaskStore sort implementation (can parallelize)
- T047-T049: CLI sort options (can parallelize)
- User story validations are independent

---

## Parallel Example: Foundational Tasks

```bash
# These tasks can run in parallel:
Task: "Create TaskPriority enum in src/models/task.py"
Task: "Create TaskCategory enum in src/models/task.py"
Task: "Update TaskStore.add() to accept new fields"
Task: "Update TaskStore.update() to accept new fields"
```

---

## Parallel Example: CLI Options

```bash
# Within US1, these can run in parallel:
Task: "Add --priority option to add command"
Task: "Add --category option to add command"
Task: "Add --due-date option to add command"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (T001-T011)
2. Complete Phase 3: User Story 1 (T012-T021)
3. **STOP and VALIDATE**: Test adding tasks with attributes
4. If working, proceed to additional stories

### Incremental Delivery

1. Complete Foundational → Data model ready
2. Add US1 → Can create tasks with attributes (MVP!)
3. Add US2 → Can update task attributes
4. Add US3 → Can filter tasks
5. Add US4 → Can sort tasks
6. Add US5 → Can view all attributes
7. Polish → Edge cases and compatibility

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 0 | Project already configured |
| Phase 2: Foundational | 11 | Enums, model updates, store updates |
| Phase 3: US1 | 10 | Add command with new options + validation |
| Phase 4: US2 | 10 | Update command with new options + validation |
| Phase 5: US3 | 12 | Filtering in store and CLI |
| Phase 6: US4 | 11 | Sorting in store and CLI |
| Phase 7: US5 | 7 | List display updates |
| Phase 8: Polish | 7 | Compatibility, edge cases, integration |
| **Total** | **68** | |

---

## Notes

- **[P]** tasks = different files, no dependencies on incomplete tasks
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently testable after Foundational phase
- Validate with actual CLI commands, not just unit tests
- Stop at any checkpoint to validate the current state
- Backward compatibility is critical - existing workflows must not break

---

## Addendum: Gap Closure Tasks (2026-01-01)

### Issue Identified

Post-implementation review revealed that while all 68 tasks were marked [X] complete, two features specified in the original requirements were **incompletely implemented**:

1. **Due Date Filtering** - Specified in User Story 3 (US3): "Filter tasks by status, priority, category, **and due date**"
2. **Keyword Search** - Specified in Functional Requirement FR-04: "Search tasks by keyword"

### Missing Implementation Details

**What was implemented in initial phase:**
- ✅ T032-T034: TaskFilter dataclass created (but without due_date and keyword fields)
- ✅ T033: TaskStore.filter() method implemented (but only for status, priority, category)
- ✅ T035-T037: CLI filter options added (but not for due-date or keyword)

**What was missing:**
- ❌ Due date field in TaskFilter
- ❌ Keyword field in TaskFilter
- ❌ Due date filtering logic in TaskStore.filter()
- ❌ Keyword search logic in TaskStore.filter()
- ❌ --due-date option in list command
- ❌ --search option in list command

### Gap Closure Tasks (Completed 2026-01-01)

- [X] T069 [P] [US3] Add due_date field to TaskFilter dataclass in src/storage/task_store.py
- [X] T070 [P] [US3] Add keyword field to TaskFilter dataclass in src/storage/task_store.py
- [X] T071 [US3] Implement due_date filtering logic in TaskStore.filter() method in src/storage/task_store.py
- [X] T072 [US3] Implement keyword search logic (title and description) in TaskStore.filter() method in src/storage/task_store.py
- [X] T073 [P] [US3] Add --due-date option to list command in src/cli/commands.py
- [X] T074 [P] [US3] Add --search option to list command in src/cli/commands.py
- [X] T075 [US3] Add date parsing and validation for --due-date in list command handler in src/cli/commands.py
- [X] T076 [US3] Add keyword assignment for --search in list command handler in src/cli/commands.py
- [X] T077 [US3] Test due date filtering with `uv run todo list --due-date 2026-01-10`
- [X] T078 [US3] Test keyword search with `uv run todo list --search "milk"`
- [X] T079 [US3] Test combined filtering with `uv run todo list --due-date 2026-01-10 --search "appointment"`
- [X] T080 [US3] Verify case-insensitive search with `uv run todo list --search "MILK"`

### Updated Task Summary

| Phase | Original Count | Gap Closure | New Total |
|-------|----------------|-------------|-----------|
| Phase 1: Setup | 0 | 0 | 0 |
| Phase 2: Foundational | 11 | 0 | 11 |
| Phase 3: US1 | 10 | 0 | 10 |
| Phase 4: US2 | 10 | 0 | 10 |
| Phase 5: US3 | 12 | **+12** | **24** |
| Phase 6: US4 | 11 | 0 | 11 |
| Phase 7: US5 | 7 | 0 | 7 |
| Phase 8: Polish | 7 | 0 | 7 |
| **Total** | **68** | **+12** | **80** |

### Files Modified in Gap Closure

- `src/storage/task_store.py:23-30` - Extended TaskFilter with due_date and keyword
- `src/storage/task_store.py:232-237` - Implemented due_date and keyword filtering
- `src/cli/commands.py:105-106` - Added --due-date and --search CLI options
- `src/cli/commands.py:130-140` - Added parsing and validation logic

### Status: Complete

All features from the original specification (including due-date filtering and keyword search) are now fully implemented and tested. User Story 3 (Filter Tasks) is 100% complete.
