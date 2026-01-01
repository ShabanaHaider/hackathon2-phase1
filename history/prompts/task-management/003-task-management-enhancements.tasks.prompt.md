---
id: "008"
title: "Task Management Enhancements"
stage: "tasks"
date: "2026-01-01"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "task-management"
branch: "003-task-persistence"
user: "(local user)"
command: "/sp.tasks"
labels: [tasks, feature-implementation]
links:
  spec: "002"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - specs/003-task-persistence/tasks.md
tests: []
---

## Prompt

**Task Management Enhancements:**

**Task 1: Enhance Task Addition**
- Modify `add` command to:
  - Accept `priority` and `category` inputs.
  - Validate due date format (YYYY-MM-DD).
  - Store priority, category, and due date.

**Task 2: Modify Task Listing**
- Modify `list` command to:
  - Support filtering by status, priority, and category.
  - Support sorting by due date, priority, or title.

**Task 3: Enhance Task Update**
- Modify `update` command to:
  - Allow updating of priority, category, and due date.

**Task 4: Testing and Validation**
- Write test cases to verify new features, ensuring tasks are correctly categorized, filtered, and sorted.

## Response snapshot

Created comprehensive implementation task list at `specs/003-task-persistence/tasks.md`:

**Task Organization (68 tasks total):**

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1: Setup | 0 | Project already configured |
| Phase 2: Foundational | 11 | TaskPriority/TaskCategory enums, Task model updates, TaskStore updates |
| Phase 3: US1 | 10 | Add command with --priority, --category, --due-date options |
| Phase 4: US2 | 10 | Update command with new attribute options |
| Phase 5: US3 | 12 | Filter by status/priority/category |
| Phase 6: US4 | 11 | Sort by due_date/priority/title |
| Phase 7: US5 | 7 | Display all attributes in list output |
| Phase 8: Polish | 7 | Backward compatibility, edge cases, integration |

**Key Implementation Details:**
- Tasks organized by user story for independent testability
- Parallel execution opportunities identified within each phase
- Each task includes exact file paths for implementation
- MVP scope: Phase 2 + Phase 3 (User Story 1)

**User Story Mapping:**
- US1 (P1): Add tasks with attributes
- US2 (P1): Update task attributes
- US3 (P2): Filter tasks
- US4 (P2): Sort tasks
- US5 (P2): View task details

## Outcome

- ✅ Impact: 68 implementation tasks generated and organized
- 🧪 Tests: 27 test tasks included across user stories
- 📁 Files: specs/003-task-persistence/tasks.md (313 lines, 68 tasks)
- 🔁 Next prompts: /sp.implement to execute tasks
- 🧠 Reflection: Tasks cover all 5 user stories with parallelization opportunities

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
