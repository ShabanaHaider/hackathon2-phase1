# Tasks: Task Persistence

**Input**: Design documents from `specs/003-task-persistence/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project is already set up - no setup tasks needed for this bug fix

**Note**: This is a minimal bug fix - existing project structure is sufficient

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core persistence infrastructure that MUST be complete before any user story can be verified

**CRITICAL**: No user story work can be fully verified until this phase is complete

### Implementation for Phase 2

- [ ] T001 Add Task.from_dict() classmethod in src/models/task.py
- [ ] T002 Add storage_file parameter and _load() method in src/storage/task_store.py
- [ ] T003 Add _save() method with atomic write in src/storage/task_store.py
- [ ] T004 Call _load() on TaskStore initialization in src/storage/task_store.py
- [ ] T005 Call _save() after add() mutation in src/storage/task_store.py
- [ ] T006 Call _save() after update() mutation in src/storage/task_store.py
- [ ] T007 Call _save() after delete() mutation in src/storage/task_store.py

**Checkpoint**: Foundation ready - persistence infrastructure is in place

---

## Phase 3: User Story 1 - Add Tasks That Persist (Priority: P1)

**Goal**: Tasks added in one CLI invocation are visible in subsequent invocations with sequential IDs

**Independent Test**: Run `todo add "Buy milk"`, then `todo list` - task 1 should appear

### Implementation for User Story 1

- [ ] T008 [US1] Verify task persistence by running add and list in separate CLI invocations

**Checkpoint**: User Story 1 validated - tasks persist between CLI invocations

---

## Phase 4: User Story 2 - Sequential IDs (Priority: P1)

**Goal**: Task IDs increment sequentially across CLI invocations (1, 2, 3...)

**Independent Test**: Add 3 tasks in separate CLI invocations - IDs should be 1, 2, 3

### Implementation for User Story 2

- [ ] T009 [US2] Verify ID persistence by adding tasks in separate CLI invocations

**Checkpoint**: User Story 2 validated - IDs are sequential across sessions

---

## Phase 5: User Story 3 - CRUD Operations Persist (Priority: P2)

**Goal**: Update, complete, and delete operations persist across CLI invocations

**Independent Test**: Complete task 1, delete task 2, update task 3 - verify changes persist

### Implementation for User Story 3

- [ ] T010 [US3] Verify complete operation persists by running complete and list in separate CLI invocations
- [ ] T011 [US3] Verify delete operation persists by running delete and list in separate CLI invocations
- [ ] T012 [US3] Verify update operation persists by running update and list in separate CLI invocations

**Checkpoint**: User Story 3 validated - all CRUD operations persist

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge case handling and robustness

- [ ] T013 Handle missing storage directory gracefully in src/storage/task_store.py
- [ ] T014 Handle corrupted storage file gracefully in src/storage/task_store.py
- [ ] T015 Run full test suite to validate all persistence scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - skipped for this bug fix
- **Foundational (Phase 2)**: No dependencies - can start immediately
- **User Stories (Phases 3-5)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - core task persistence
- **User Story 2 (P1)**: Depends on Foundational (Phase 2) - ID sequence persistence
- **User Story 3 (P2)**: Depends on Foundational (Phase 2) - CRUD operation persistence

### Within Each User Story

- Foundation must complete before any story can be validated
- Each story validation is independent and can be tested separately

### Parallel Opportunities

- All Foundational tasks (T001-T007) work on different methods but must be complete before validation
- User story validations (T008-T012) are independent and can be run in any order

---

## Parallel Example: Foundational Tasks

```bash
# These tasks modify different methods but must all complete before validation:
Task: "Add Task.from_dict() classmethod in src/models/task.py"
Task: "Add _load() and _save() methods in src/storage/task_store.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (T001-T007)
2. Complete Phase 3: User Story 1 validation (T008)
3. **STOP and VALIDATE**: Test task persistence
4. If working, proceed to additional stories

### Incremental Delivery

1. Complete Foundational → Persistence infrastructure ready
2. Add US1 validation → Tasks persist (MVP!)
3. Add US2 validation → Sequential IDs work
4. Add US3 validation → CRUD operations persist
5. Polish → Edge case handling

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 0 | Project already configured |
| Phase 2: Foundational | 7 | Persistence infrastructure |
| Phase 3: US1 | 1 | Task persistence validation |
| Phase 4: US2 | 1 | Sequential ID validation |
| Phase 5: US3 | 3 | CRUD persistence validation |
| Phase 6: Polish | 3 | Edge cases and testing |
| **Total** | **15** | |

---

## Notes

- **[P]** tasks = different files, no dependencies on incomplete tasks
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently testable after Foundational phase
- Validate with actual CLI commands, not just unit tests
- Stop at any checkpoint to validate the current state
