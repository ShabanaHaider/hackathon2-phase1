---
description: "Task list for Advanced Features - Recurring Tasks, Due Date Reminders, and Interactive CLI"
---

# Tasks: Advanced Features - Recurring Tasks, Due Date Reminders, and Interactive CLI

**Input**: Design documents from `/specs/001-advanced-features/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted per template guidelines.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure as defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [x] T001 Add plyer dependency to pyproject.toml for desktop notifications
- [x] T002 [P] Create src/models/recurrence.py module structure
- [x] T003 [P] Create src/models/reminder.py module structure
- [x] T004 [P] Create src/services/reminder_service.py module structure
- [x] T005 [P] Create src/services/recurrence_service.py module structure
- [x] T006 [P] Create src/cli/menu.py module structure
- [x] T007 [P] Create src/cli/prompts.py module structure
- [x] T008 [P] Create src/cli/validation.py module structure
- [x] T009 [P] Create src/cli/formatters.py module structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 Extend Task model in src/models/task.py with due_time field (Optional[time])
- [ ] T011 Add reminder_intervals field to Task model in src/models/task.py (List[int])
- [ ] T012 Add recurrence field to Task model in src/models/task.py (Optional[RecurrencePattern])
- [ ] T013 Add completed_at field to Task model in src/models/task.py (Optional[datetime])
- [ ] T014 Add parent_recurrence_id field to Task model in src/models/task.py (Optional[int])
- [ ] T015 Implement RecurrenceInterval enum in src/models/recurrence.py (DAILY, WEEKLY, MONTHLY, CUSTOM)
- [ ] T016 Implement RecurrencePattern dataclass in src/models/recurrence.py with interval_type and interval_value fields
- [ ] T017 Implement calculate_next_occurrence method in RecurrencePattern class in src/models/recurrence.py
- [ ] T018 Implement Reminder dataclass in src/models/reminder.py with task_id, reminder_time, minutes_before, sent fields
- [ ] T019 Update Task.to_dict() method in src/models/task.py to serialize new fields
- [ ] T020 Update Task.from_dict() method in src/models/task.py to deserialize new fields

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 4 - Refined Interactive CLI Interface (Priority: P1) 🎯 MVP Component

**Goal**: Provide menu-driven CLI interface with interactive prompts and comprehensive input validation

**Independent Test**: Launch CLI, navigate menu, add task with invalid inputs (rejected with errors), successfully add task with guided prompts

### Implementation for User Story 4

- [ ] T021 [P] [US4] Implement ValidationError exception class in src/cli/validation.py
- [ ] T022 [P] [US4] Implement validate_priority function in src/cli/validation.py (accepts high/medium/low, case-insensitive)
- [ ] T023 [P] [US4] Implement validate_category function in src/cli/validation.py (accepts work/home, case-insensitive)
- [ ] T024 [P] [US4] Implement validate_due_date function in src/cli/validation.py (YYYY-MM-DD format, rejects >10 years future)
- [ ] T025 [P] [US4] Implement validate_due_time function in src/cli/validation.py (HH:MM format, 24-hour)
- [ ] T026 [P] [US4] Implement validate_recurrence function in src/cli/validation.py (daily/weekly/monthly/custom or positive integer)
- [ ] T027 [P] [US4] Implement validate_reminder_interval function in src/cli/validation.py (positive integer, max 5 per task)
- [ ] T028 [P] [US4] Implement validate_task_id function in src/cli/validation.py (positive integer, exists in store)
- [ ] T029 [P] [US4] Implement validate_title function in src/cli/validation.py (not empty, ≤255 chars)
- [ ] T030 [P] [US4] Implement validate_description function in src/cli/validation.py (≤2000 chars)
- [ ] T031 [US4] Implement prompt_with_validation helper in src/cli/prompts.py (retries up to 3 times, returns None on failure)
- [ ] T032 [US4] Implement prompt_for_title in src/cli/prompts.py using validate_title
- [ ] T033 [US4] Implement prompt_for_description in src/cli/prompts.py (optional field, skip on empty)
- [ ] T034 [US4] Implement prompt_for_priority in src/cli/prompts.py using validate_priority with default="medium"
- [ ] T035 [US4] Implement prompt_for_category in src/cli/prompts.py using validate_category with default="uncategorized"
- [ ] T036 [US4] Implement show_main_menu function in src/cli/menu.py (displays 6 options: Add/View/Update/Delete/Complete/Exit)
- [ ] T037 [US4] Implement main_menu_loop function in src/cli/menu.py with KeyboardInterrupt handling (Ctrl+C confirms exit at menu)
- [ ] T038 [US4] Implement handle_add_task function in src/cli/menu.py that calls prompt functions and creates task
- [ ] T039 [US4] Implement handle_view_tasks function in src/cli/menu.py with interactive filter/sort options
- [ ] T040 [US4] Implement handle_update_task function in src/cli/menu.py with task ID prompt and field selection
- [ ] T041 [US4] Implement handle_delete_task function in src/cli/menu.py with task ID prompt and confirmation
- [ ] T042 [US4] Implement handle_complete_task function in src/cli/menu.py with task ID prompt
- [ ] T043 [US4] Update main entry point in src/cli/commands.py to launch main_menu_loop() by default
- [ ] T044 [US4] Add KeyboardInterrupt handling in prompt functions to return to main menu (cancel operation, not exit app)

**Checkpoint**: Interactive CLI menu system is functional with validation; users can add/view/update/delete/complete tasks via guided prompts

---

## Phase 4: User Story 1 - Set Due Dates with Time-Based Reminders (Priority: P1) 🎯 MVP Component

**Goal**: Allow users to set due dates/times and receive desktop notifications before deadlines

**Independent Test**: Create task with due date "2026-01-10 17:00" and reminder "15 minutes before", verify notification at 16:45

### Implementation for User Story 1

- [ ] T045 [P] [US1] Implement update_due_time method in Task class in src/models/task.py (validates due_date exists)
- [ ] T046 [P] [US1] Implement set_reminder_intervals method in Task class in src/models/task.py (validates due_date exists, max 5 reminders)
- [ ] T047 [P] [US1] Implement get_full_due_datetime method in Task class in src/models/task.py (combines due_date + due_time)
- [ ] T048 [P] [US1] Implement is_overdue method in Task class in src/models/task.py (checks if past due and incomplete)
- [ ] T049 [P] [US1] Implement calculate_reminder_times method in Task class in src/models/task.py (returns List[datetime] for reminders)
- [ ] T050 [US1] Implement ReminderService class in src/services/reminder_service.py with __init__, start, stop, _check_reminders methods
- [ ] T051 [US1] Add background daemon thread to ReminderService in src/services/reminder_service.py (polls every 10 seconds)
- [ ] T052 [US1] Implement refresh_reminders method in ReminderService in src/services/reminder_service.py (rebuilds priority queue from tasks)
- [ ] T053 [US1] Implement _send_notification method in ReminderService in src/services/reminder_service.py using plyer
- [ ] T054 [US1] Add console fallback in _send_notification if plyer unavailable in src/services/reminder_service.py
- [ ] T055 [US1] Implement prompt_for_due_date in src/cli/prompts.py using validate_due_date (optional field)
- [ ] T056 [US1] Implement prompt_for_due_time in src/cli/prompts.py using validate_due_time (optional, requires due_date)
- [ ] T057 [US1] Implement prompt_for_reminders in src/cli/prompts.py using validate_reminder_interval (optional, multi-value)
- [ ] T058 [US1] Update handle_add_task in src/cli/menu.py to prompt for due_date, due_time, reminders
- [ ] T059 [US1] Update handle_update_task in src/cli/menu.py to allow updating due_date, due_time, reminders
- [ ] T060 [US1] Implement format_due_datetime function in src/cli/formatters.py (displays "YYYY-MM-DD HH:MM" or "YYYY-MM-DD" if no time)
- [ ] T061 [US1] Implement format_overdue_indicator function in src/cli/formatters.py (returns "[OVERDUE]" for overdue tasks)
- [ ] T062 [US1] Update handle_view_tasks in src/cli/menu.py to display due dates with format_due_datetime and overdue indicators
- [ ] T063 [US1] Add filter options in handle_view_tasks for --overdue, --due-today, --due-this-week in src/cli/menu.py
- [ ] T064 [US1] Implement sort by due date in handle_view_tasks (overdue first, then ascending) in src/cli/menu.py
- [ ] T065 [US1] Initialize ReminderService in main_menu_loop startup in src/cli/menu.py
- [ ] T066 [US1] Call reminder_service.refresh_reminders() after add/update/delete/complete operations in src/cli/menu.py
- [ ] T067 [US1] Ensure reminder_service.stop() on application exit in src/cli/menu.py

**Checkpoint**: Users can set due dates/times, configure reminders, receive desktop notifications, and see overdue tasks highlighted

---

## Phase 5: User Story 2 - Create and Manage Recurring Tasks (Priority: P2)

**Goal**: Allow users to create tasks that repeat at regular intervals (daily, weekly, monthly, custom)

**Independent Test**: Create recurring task "Weekly meeting" repeating every 7 days, mark complete, verify new instance created

### Implementation for User Story 2

- [ ] T068 [P] [US2] Implement update_recurrence method in Task class in src/models/task.py (sets recurrence pattern)
- [ ] T069 [P] [US2] Implement to_dict and from_dict methods for RecurrencePattern in src/models/recurrence.py
- [ ] T070 [P] [US2] Implement __str__ method for RecurrencePattern in src/models/recurrence.py (returns "Repeats every X days")
- [ ] T071 [US2] Implement RecurrenceService class in src/services/recurrence_service.py with create_next_instance method
- [ ] T072 [US2] In create_next_instance, calculate next due date using recurrence.calculate_next_occurrence in src/services/recurrence_service.py
- [ ] T073 [US2] In create_next_instance, copy task attributes (title, description, priority, category, recurrence) to new instance in src/services/recurrence_service.py
- [ ] T074 [US2] In create_next_instance, set parent_recurrence_id to original task ID in src/services/recurrence_service.py
- [ ] T075 [US2] In create_next_instance, preserve due_time and reminder_intervals if set in src/services/recurrence_service.py
- [ ] T076 [US2] Implement prompt_for_recurrence in src/cli/prompts.py using validate_recurrence (optional field, daily/weekly/monthly/custom)
- [ ] T077 [US2] Implement prompt_for_recurrence_days in src/cli/prompts.py for custom intervals (only if recurrence=custom)
- [ ] T078 [US2] Update handle_add_task in src/cli/menu.py to prompt for recurrence and recurrence_days
- [ ] T079 [US2] Update handle_update_task in src/cli/menu.py to allow updating recurrence pattern
- [ ] T080 [US2] Implement format_recurrence function in src/cli/formatters.py (displays "Daily", "Weekly", "3d", etc.)
- [ ] T081 [US2] Update handle_view_tasks in src/cli/menu.py to display recurrence patterns using format_recurrence
- [ ] T082 [US2] Add --recurring-only filter option in handle_view_tasks in src/cli/menu.py
- [ ] T083 [US2] Update handle_complete_task in src/cli/menu.py to check if task is recurring
- [ ] T084 [US2] If recurring, call recurrence_service.create_next_instance after marking complete in src/cli/menu.py
- [ ] T085 [US2] Display message showing next instance created with due date in src/cli/menu.py
- [ ] T086 [US2] Update handle_delete_task in src/cli/menu.py to display note about recurring task deletion (current instance only)

**Checkpoint**: Users can create recurring tasks, mark them complete (new instance auto-created), and view recurrence patterns

---

## Phase 6: User Story 3 - Combined Recurring + Reminders (Priority: P3)

**Goal**: Support recurring tasks with due times and reminders for each occurrence

**Independent Test**: Create recurring task "Weekly report" every Friday 5 PM with 1-hour reminder, mark complete, verify next instance has due time and reminder

### Implementation for User Story 3

- [ ] T087 [US3] Validate in handle_add_task that if recurrence + due_time set, both are compatible in src/cli/menu.py
- [ ] T088 [US3] Ensure create_next_instance preserves due_time when creating recurring instance in src/services/recurrence_service.py
- [ ] T089 [US3] Ensure create_next_instance preserves reminder_intervals when creating recurring instance in src/services/recurrence_service.py
- [ ] T090 [US3] After creating next instance, call reminder_service.refresh_reminders() to schedule new reminders in src/cli/menu.py
- [ ] T091 [US3] Update format_recurrence to show combined info (e.g., "Weekly on Fridays 17:00") in src/cli/formatters.py
- [ ] T092 [US3] Test combined feature: recurring task with due_time and reminders, verify reminders trigger for each instance

**Checkpoint**: Recurring tasks with due times and reminders work correctly; each new instance has reminders scheduled

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, error handling, and user experience enhancements

- [ ] T093 [P] Add error handling for plyer notification failures in src/services/reminder_service.py
- [ ] T094 [P] Add thread-safe locking in ReminderService when accessing task_store in src/services/reminder_service.py
- [ ] T095 [P] Add color coding using click.style for success (green) and error (red) messages in src/cli/menu.py
- [ ] T096 [P] Add clear screen functionality (optional, platform-aware) in src/cli/menu.py
- [ ] T097 [P] Add footer hint "Press Ctrl+C to cancel" during prompts in src/cli/prompts.py
- [ ] T098 [P] Implement text truncation for long titles in table display in src/cli/formatters.py
- [ ] T099 [P] Add terminal width detection and responsive formatting in src/cli/formatters.py
- [ ] T100 Validate quickstart.md examples work with interactive menu system
- [ ] T101 Update README.md with interactive menu usage examples
- [ ] T102 Perform end-to-end testing of all user stories in interactive mode

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 4 (Phase 3)**: Depends on Foundational completion - Can proceed independently (Interactive CLI)
- **User Story 1 (Phase 4)**: Depends on Foundational completion - Can proceed in parallel with US4
- **User Story 2 (Phase 5)**: Depends on Foundational completion - Can proceed in parallel with US1/US4
- **User Story 3 (Phase 6)**: Depends on US1 AND US2 completion (combines both features)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 4 (P1 - Interactive CLI)**: Independent - Can start after Foundational (Phase 2)
- **User Story 1 (P1 - Due Dates/Reminders)**: Independent - Can start after Foundational (Phase 2)
- **User Story 2 (P2 - Recurring Tasks)**: Independent - Can start after Foundational (Phase 2)
- **User Story 3 (P3 - Combined)**: Dependent on US1 AND US2

### Within Each User Story

- Validation functions (T021-T030) can run in parallel
- Prompt functions depend on validation functions
- Menu handlers depend on prompt functions
- Services can be built in parallel with CLI components
- Integration tasks run after components complete

### Parallel Opportunities

**Phase 1 (Setup)**: All tasks marked [P] (T002-T009) can run in parallel

**Phase 2 (Foundational)**: Tasks T010-T020 must run sequentially (all modify Task model)

**Phase 3 (User Story 4)**:
- Validation functions (T021-T030) can all run in parallel
- Prompt functions (T032-T035) can run in parallel after validation complete

**Phase 4 (User Story 1)**:
- Task methods (T045-T049) can run in parallel
- ReminderService (T050-T054) can proceed independently

**Phase 5 (User Story 2)**:
- RecurrencePattern methods (T068-T070) can run in parallel
- RecurrenceService (T071-T075) can proceed independently

**Phase 7 (Polish)**: All tasks marked [P] (T093-T099) can run in parallel

---

## Parallel Example: User Story 1 (Due Dates/Reminders)

```bash
# Launch all Task model methods together:
Task: "Implement update_due_time method in src/models/task.py"
Task: "Implement set_reminder_intervals method in src/models/task.py"
Task: "Implement get_full_due_datetime method in src/models/task.py"
Task: "Implement is_overdue method in src/models/task.py"
Task: "Implement calculate_reminder_times method in src/models/task.py"

# ReminderService can be built in parallel with Task methods:
Task: "Implement ReminderService class in src/services/reminder_service.py"
```

---

## Implementation Strategy

### MVP First (Interactive CLI + Due Dates)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 4 (Interactive CLI) - Essential for UX
4. Complete Phase 4: User Story 1 (Due Dates/Reminders) - Core time management
5. **STOP and VALIDATE**: Test interactive menu with due dates and reminders
6. Deploy/demo if ready

**Rationale**: US4 (Interactive CLI) + US1 (Due Dates/Reminders) form a complete MVP that delivers core value without recurring task complexity.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 4 (Interactive CLI) → Test independently → Deploy/Demo (UX improvement!)
3. Add User Story 1 (Due Dates/Reminders) → Test independently → Deploy/Demo (MVP!)
4. Add User Story 2 (Recurring Tasks) → Test independently → Deploy/Demo
5. Add User Story 3 (Combined) → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 4 (Interactive CLI)
   - Developer B: User Story 1 (Due Dates/Reminders)
   - Developer C: User Story 2 (Recurring Tasks)
3. Developer D joins for User Story 3 after US1 + US2 complete
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Tests are NOT included per template guidelines (not explicitly requested in spec)
- Focus on iterative delivery: Get US4 + US1 working first (MVP), then add US2, then US3

---

## Task Count Summary

- **Phase 1 (Setup)**: 9 tasks
- **Phase 2 (Foundational)**: 11 tasks
- **Phase 3 (User Story 4 - Interactive CLI)**: 24 tasks
- **Phase 4 (User Story 1 - Due Dates/Reminders)**: 23 tasks
- **Phase 5 (User Story 2 - Recurring Tasks)**: 19 tasks
- **Phase 6 (User Story 3 - Combined)**: 6 tasks
- **Phase 7 (Polish)**: 10 tasks

**Total**: 102 tasks

**MVP Scope** (Phases 1-4): 67 tasks
**Full Feature** (All Phases): 102 tasks

**Parallel Opportunities**: 30+ tasks can run in parallel (marked with [P])
