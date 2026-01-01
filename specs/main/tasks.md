---

description: "Task list for replacing deprecated datetime.utcnow with timezone-aware UTC timestamps"
---

# Tasks: datetime-utcnow-migration

**Purpose**: Replace all `datetime.utcnow()` usages with `datetime.now(timezone.utc)` for Python 3.13+ compatibility

**Input**: Analysis of `src/models/task.py` and `tests/unit/test_task.py`

**Scope**:
- Replace 6 occurrences in `src/models/task.py`
- Replace 1 occurrence in `tests/unit/test_task.py`
- No behavior change - timestamps must represent the same moments in time

**Non-Goals**:
- No new features
- No API changes
- No database migrations

---

## Phase 1: Analysis & Planning

**Purpose**: Understand the scope and create a helper for consistent timestamp generation

- [X] T001 Review all datetime.utcnow occurrences in src/models/task.py
- [X] T002 Review datetime.utcnow usage in tests/unit/test_task.py
- [X] T003 Document the replacement strategy: datetime.now(timezone.utc)

---

## Phase 2: Implementation

**Purpose**: Replace deprecated datetime.utcnow with timezone-aware UTC timestamps

### Update src/models/task.py

- [X] T004 [P] Import timezone from datetime module in src/models/task.py
- [X] T005 [P] Replace field default_factory=datetime.utcnow with field(default_factory=lambda: datetime.now(timezone.utc)) for created_at in src/models/task.py:33
- [X] T006 [P] Replace field default_factory=datetime.utcnow with field(default_factory=lambda: datetime.now(timezone.utc)) for updated_at in src/models/task.py:34
- [X] T007 [P] Replace datetime.utcnow() with datetime.now(timezone.utc) in update_title method at src/models/task.py:52
- [X] T008 [P] Replace datetime.utcnow() with datetime.now(timezone.utc) in update_description method at src/models/task.py:59
- [X] T009 [P] Replace datetime.utcnow() with datetime.now(timezone.utc) in mark_complete method at src/models/task.py:64
- [X] T010 [P] Replace datetime.utcnow() with datetime.now(timezone.utc) in mark_incomplete method at src/models/task.py:69

### Update tests/unit/test_task.py

- [X] T011 [P] Import timezone from datetime in tests/unit/test_task.py
- [X] T012 [P] Replace datetime.utcnow() with datetime.now(timezone.utc) for test data creation at tests/unit/test_task.py:24

---

## Phase 3: Validation

**Purpose**: Ensure the changes work correctly without breaking existing behavior

- [X] T013 Run existing unit tests to verify no regressions: pytest tests/unit/test_task.py -v
- [X] T014 Verify datetime fields are now timezone-aware (have tzinfo set)
- [X] T015 Compare isoformat() output before/after to confirm same string representation
- [X] T016 Run the full test suite: pytest -v

---

## Phase 4: Polish

**Purpose**: Ensure code quality and future compatibility

- [X] T017 [P] Verify no other files in the project use datetime.utcnow (grep search)
- [X] T018 Update or add comments explaining timezone-aware approach for future maintainers
- [X] T019 Consider adding a module-level helper function for consistent UTC timestamp generation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Analysis)**: No dependencies - starts immediately
- **Phase 2 (Implementation)**: Depends on Phase 1 completion
- **Phase 3 (Validation)**: Depends on Phase 2 completion
- **Phase 4 (Polish)**: Depends on Phase 3 completion

### Within Each Phase

- All tasks marked [P] in Phase 2 can run in parallel (different line locations)
- Validation tasks should run sequentially
- Polish tasks marked [P] can run in parallel

### Parallel Opportunities

- T004 through T010 can all be done in parallel (different line locations in same file)
- T011 and T012 can be done in parallel with Phase 2 implementation tasks
- T017 and T018 can be done in parallel

---

## Parallel Example: Phase 2 Implementation

```bash
# These tasks modify different lines and can be done in parallel:
Task: "Import timezone from datetime module in src/models/task.py"
Task: "Replace field default_factory for created_at in src/models/task.py:33"
Task: "Replace field default_factory for updated_at in src/models/task.py:34"
Task: "Replace datetime.utcnow() in update_title method at src/models/task.py:52"
Task: "Replace datetime.utcnow() in update_description method at src/models/task.py:59"
Task: "Replace datetime.utcnow() in mark_complete method at src/models/task.py:64"
Task: "Replace datetime.utcnow() in mark_incomplete method at src/models/task.py:69"
```

---

## Implementation Strategy

### Minimal Viable Change

1. Complete Phase 1: Analysis (verify scope)
2. Complete Phase 2: All implementation tasks
3. Complete Phase 3: Validation
4. **STOP and VALIDATE**: All tests pass, no behavior change

### Quick Execution

1. Phase 1 tasks can be done mentally (quick review)
2. Phase 2: Replace all occurrences in one session
3. Phase 3: Run tests to verify
4. Phase 4: Optional polish items

---

## Notes

- [P] tasks = different file locations, can be done in parallel
- All replacements must use `datetime.now(timezone.utc)` for consistency
- The `isoformat()` method will now include `+00:00` suffix - this is correct behavior
- No application behavior should change - same timestamps, just with timezone info
- Python 3.2+ supports `datetime.now(timezone.utc)`, ensuring broad compatibility
