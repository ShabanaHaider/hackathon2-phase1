# Implementation Plan: Task Management CLI Enhancements

**Branch**: `003-task-management` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-task-persistence/spec.md`

## Summary

Extend the Todo CLI with advanced task management features including priority levels (high/medium/low), task categories (work/home), and due dates (YYYY-MM-DD). The implementation will add filtering and sorting capabilities to the list command while maintaining full backward compatibility with existing commands. This requires updates to the Task model, TaskStore, and CLI commands to support the new attributes.

## Technical Context

**Language/Version**: Python 3.13+ (per constitution)
**Primary Dependencies**: Click (CLI framework), no new dependencies required
**Storage**: File-based JSON persistence at `~/.todo/tasks.json` (existing)
**Testing**: pytest (existing test infrastructure)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project (CLI application)
**Performance Goals**: Minimal - CLI tool with in-memory storage, operations < 100ms
**Constraints**: Maintain backward compatibility, use existing storage format
**Scale/Scope**: Single-user, < 1000 tasks expected

### Technical Decisions (Resolved)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Priority enum | StrEnum or Literal | Use Python's enum for type safety, consistent with TaskStatus |
| Category enum | StrEnum or Literal | Use enum similar to priority for consistency |
| Due date storage | ISO 8601 string in JSON | Compatible with existing storage format, datetime parsing |
| Filtering approach | Store-level filtering | Enables reuse and testability |
| Sorting approach | Store-level sorting | Consistent with filtering approach |

### Unknowns Resolved

1. **Priority representation**: Use Enum (TaskPriority) matching TaskStatus pattern
2. **Category representation**: Use Enum (TaskCategory) matching TaskStatus pattern
3. **Due date handling**: Store as ISO string in JSON, parse as date in Python
4. **Filtering/sorting**: Implement in TaskStore for consistency with existing patterns

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Rule | Status | Notes |
|------|--------|-------|
| CLI-only interaction | ✅ PASS | All features through CLI commands |
| Python 3.13+ | ✅ PASS | Existing codebase uses Python 3.13+ |
| UV for environment | ✅ PASS | Existing setup uses UV |
| Claude Code for impl | ✅ PASS | Implementation via /sp.implement |
| No manual coding | ✅ PASS | All code via agent execution |
| Spec-Kit Plus artifacts | ✅ PASS | All phases documented |
| Task ID traceability | ✅ PASS | Tasks will reference spec requirements |
| No code without Task ID | ✅ PASS | Enforced during /sp.tasks phase |

### Constitution Violations

None identified. This feature aligns with constitution scope items 6, 7, 8.

## Project Structure

### Documentation (this feature)

```text
specs/003-task-persistence/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (this file)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── cli-commands.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task entity with priority, category, due_date
├── storage/
│   └── task_store.py    # TaskStore with filtering/sorting methods
├── cli/
│   └── commands.py      # Updated CLI commands with new options
tests/
├── unit/
│   ├── test_task.py     # Task model tests
│   └── test_task_store.py
└── integration/
    └── test_cli.py      # CLI integration tests
```

**Structure Decision**: Single project structure. The existing codebase uses this pattern. New files follow the established conventions in models/, storage/, and cli/ directories.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No complexity tracking required - feature fits within existing architecture.

## Phase 0: Research Summary

### Key Findings

1. **Task Model Extension**: Add priority (Enum), category (Enum), due_date (Optional[date]) fields to Task dataclass
2. **TaskStore Updates**: Add filter() and sort() methods supporting multiple criteria
3. **CLI Updates**: Add --priority, --category, --due options to add/update commands; add --filter-by, --sort-by to list command
4. **Backward Compatibility**: Existing tasks without new fields default to medium priority, uncategorized, no due date
5. **Validation**: Click choice constraints for enum values, datetime parsing for dates

### Implementation Approach

- Extend Task dataclass with new fields and validation
- Add TaskPriority and TaskCategory enums
- Update TaskStore.add() and TaskStore.update() to accept new fields
- Implement TaskStore.filter() and TaskStore.sort() methods
- Update CLI commands with new options
- Add unit tests for new functionality

## Phase 1: Design Artifacts

### Generated Files

- `data-model.md`: Entity definitions and relationships
- `contracts/cli-commands.md`: CLI command signatures and contracts
- `quickstart.md`: Usage guide for new features

### Next Steps

After plan approval, run `/sp.tasks` to generate implementation tasks.

---

## Addendum: Implementation Gap Closure (2026-01-01)

### Issue Discovered

During post-implementation review, two features specified in the original requirements were found to be **incompletely implemented** during the initial `/sp.implement` execution:

1. **Due Date Filtering**: Specified in User Story 3 (US3) - "Filter tasks by status, priority, category, **and due date**"
2. **Keyword Search**: Specified in Functional Requirement FR-04 - "Search tasks by keyword"

### Root Cause

The initial implementation (all 68 tasks marked complete) included:
- ✅ Due date field in Task model
- ✅ Due date option in add/update commands
- ✅ Due date display in list command
- ❌ Missing: Due date filtering in list command
- ❌ Missing: Keyword search in list command

### Implementation Completed (2026-01-01)

**Files Modified:**
- `src/storage/task_store.py:23-30` - Extended TaskFilter with due_date and keyword fields
- `src/storage/task_store.py:232-237` - Implemented due_date and keyword filtering logic
- `src/cli/commands.py:105-106` - Added --due-date and --search CLI options
- `src/cli/commands.py:130-140` - Added parsing and validation logic

**Features Added:**
1. **Due Date Filtering** (`--due-date` / `-D`):
   - Filter tasks by exact due date match
   - Format: YYYY-MM-DD
   - Validation: ISO date format checking

2. **Keyword Search** (`--search` / `-s`):
   - Case-insensitive search across title and description
   - Partial match support
   - Combines with other filters

**Testing Verified:**
```bash
# Due date filtering
uv run todo list --due-date 2026-01-10

# Keyword search
uv run todo list --search "milk"

# Combined filtering
uv run todo list --due-date 2026-01-10 --search "appointment"
```

### Status: Complete

All features from the original specification are now fully implemented. The feature is ready for production use.
