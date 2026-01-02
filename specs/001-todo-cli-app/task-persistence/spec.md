# Feature Specification: Task Management CLI Enhancements

**Feature Branch**: `003-task-management`
**Created**: 2026-01-01
**Status**: Draft
**Input**: Extend Todo CLI with advanced task management features including priority, category, due dates, filtering, and sorting.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add tasks with priority, category, and due date (Priority: P1)

As a user, I want to add tasks with priority, category, and due date attributes, so that I can organize and prioritize my todo list effectively.

**Why this priority**: This is the foundational feature that enables all other advanced functionality. Without proper task attribute input, filtering and sorting have no purpose.

**Independent Test**: Can be tested by adding a task with all attributes and verifying they are stored and displayed correctly.

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** user runs `todo add "Buy milk" --priority high --category home --due 2026-01-15`, **Then** task is created with priority=high, category=home, and due_date=2026-01-15.
2. **Given** a task is being added, **When** user provides invalid priority value, **Then** system displays error and task is not created.
3. **Given** a task is being added, **When** user provides invalid date format, **Then** system displays error and task is not created.
4. **Given** a task is being added, **When** user provides no optional attributes, **Then** defaults are applied (priority=medium, category=uncategorized, no due date).

---

### User Story 2 - Update task attributes (Priority: P1)

As a user, I want to update the priority, category, and due date of existing tasks, so that I can adjust task details as priorities change.

**Why this priority**: Task attributes change over time; users need flexibility to modify them without recreating tasks.

**Independent Test**: Can be tested by updating a task's attributes and verifying the changes persist.

**Acceptance Scenarios**:

1. **Given** task 1 exists with priority=low, **When** user runs `todo update 1 --priority high`, **Then** task 1 now has priority=high.
2. **Given** task 1 exists with no due date, **When** user runs `todo update 1 --due 2026-02-01`, **Then** task 1 now has due_date=2026-02-01.
3. **Given** task 1 exists, **When** user runs `todo update 1 --category work`, **Then** task 1 now has category=work.
4. **Given** task 1 exists, **When** user clears the due date with `--due ""`, **Then** task 1 no longer has a due date.

---

### User Story 3 - Filter tasks (Priority: P2)

As a user, I want to filter tasks by status, priority, and category, so that I can focus on specific subsets of my todo list.

**Why this priority**: Filtering enables users to find relevant tasks quickly without scrolling through all tasks.

**Independent Test**: Can be tested by creating tasks with different attributes and verifying only matching tasks are displayed.

**Acceptance Scenarios**:

1. **Given** multiple tasks exist with different priorities, **When** user runs `todo list --priority high`, **Then** only tasks with priority=high are displayed.
2. **Given** multiple tasks exist with different categories, **When** user runs `todo list --category work`, **Then** only tasks with category=work are displayed.
3. **Given** multiple tasks exist with different statuses, **When** user runs `todo list --status pending`, **Then** only pending tasks are displayed.
4. **Given** multiple tasks exist, **When** user runs `todo list --priority high --category work`, **Then** only tasks matching both criteria are displayed.
5. **Given** no tasks match the filter, **When** user runs `todo list --priority high`, **Then** system displays "No tasks found" message.

---

### User Story 4 - Sort tasks (Priority: P2)

As a user, I want to sort tasks by due date, priority, or title, so that I can view my tasks in an order that makes sense for my workflow.

**Why this priority**: Sorting helps users identify urgent and important tasks at a glance.

**Independent Test**: Can be tested by creating tasks with different attributes and verifying they appear in the expected order.

**Acceptance Scenarios**:

1. **Given** multiple tasks exist with due dates, **When** user runs `todo list --sort due`, **Then** tasks are ordered by due date (earliest first).
2. **Given** multiple tasks exist with different priorities, **When** user runs `todo list --sort priority`, **Then** tasks are ordered by priority (high > medium > low).
3. **Given** multiple tasks exist, **When** user runs `todo list --sort title`, **Then** tasks are ordered alphabetically by title.
4. **Given** tasks without due dates exist, **When** user sorts by due date, **Then** tasks without due dates appear at the end.

---

### User Story 5 - View task details with all attributes (Priority: P2)

As a user, I want to see the priority, category, and due date of each task when listing tasks, so that I have complete information about my todo list at a glance.

**Why this priority**: Visibility of all task attributes enables better task management decisions.

**Independent Test**: Can be tested by adding tasks with various attributes and verifying the list view displays them correctly.

**Acceptance Scenarios**:

1. **Given** a task exists with priority=high, category=work, due_date=2026-01-15, **When** user runs `todo list`, **Then** the task display includes priority, category, and due date columns.
2. **Given** a task exists without a due date, **When** user runs `todo list`, **Then** the due date column shows "None" or "-" for that task.
3. **Given** multiple tasks exist, **When** user runs `todo list`, **Then** all tasks are displayed with their respective attributes in a readable format.

---

### Edge Cases

- What happens when a due date is in the past?
- How does the system handle duplicate category names (case sensitivity)?
- What happens if the user provides an invalid date value (e.g., 2026-02-30)?
- How does the system handle priority values other than high/medium/low?
- What happens when filtering by an attribute that no tasks have?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support three priority levels: high, medium, and low. Default priority is medium.
- **FR-002**: System MUST support two category types: work and home. Default category is uncategorized.
- **FR-003**: System MUST accept due dates in YYYY-MM-DD format. Due date is optional.
- **FR-004**: System MUST validate priority values and reject invalid values with an error message.
- **FR-005**: System MUST validate date format and reject invalid dates with an error message.
- **FR-006**: System MUST support filtering by one or more attributes: status (pending/completed), priority (high/medium/low), category (work/home).
- **FR-007**: System MUST support sorting by: due date (ascending), priority (high>medium>low), title (alphabetical).
- **FR-008**: System MUST maintain backward compatibility with all existing commands (add, list, update, delete, complete, incomplete).
- **FR-009**: System MUST persist all new task attributes (priority, category, due_date) to storage.
- **FR-010**: System MUST allow clearing the due date via update command.

### Key Entities

- **Task**: Represents a todo item with id, title, status (pending/completed), priority (high/medium/low), category (work/home/uncategorized), due_date (optional YYYY-MM-DD), created_at, updated_at.
- **Task Display Format**: Table or list view showing ID, title, priority, category, due date, and status.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create tasks with priority, category, and due date (100% success rate for valid inputs).
- **SC-002**: Users can update any combination of task attributes (100% success rate for valid inputs).
- **SC-003**: Filtering returns only tasks matching specified criteria (100% accuracy).
- **SC-004**: Sorting orders tasks correctly according to selected criteria (100% accuracy).
- **SC-005**: All existing commands continue to function without modification (100% backward compatibility).
- **SC-006**: All new attributes persist correctly across CLI invocations (100% persistence rate).
