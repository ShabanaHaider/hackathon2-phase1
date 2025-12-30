# Quickstart Guide: Todo CLI Application

**Feature**: 001-todo-cli-app
**Created**: 2025-12-30

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Installation

1. **Clone the repository** (if not already done)
2. **Initialize the project with UV**:

```bash
uv init
```

3. **Add project dependencies** (click for CLI parsing):

```bash
uv add click pytest
```

4. **Verify installation**:

```bash
python -m src --help
```

## Development Workflow

This project follows the Spec-Driven Development (SDD) workflow:

```
Constitution → Specification → Plan → Tasks → Implementation
```

### Current Phase

You are viewing the **Plan** phase artifacts:
- `plan.md` - Architectural decisions and project structure
- `data-model.md` - Entity definitions and storage contracts
- `contracts/cli-commands.md` - CLI interface specifications
- `quickstart.md` - This file (development setup)

### Next Steps

After `/sp.plan` completes, run:

```bash
/sp.tasks  # Generate executable task list
```

Then:

```bash
/sp.implement  # Execute tasks and build the application
```

## Project Structure

```
src/
├── models/
│   └── task.py          # Task entity
├── storage/
│   └── task_store.py    # In-memory task repository
├── cli/
│   ├── commands.py      # CLI command definitions
│   └── __init__.py
└── __init__.py

tests/
└── unit/
    ├── test_task.py
    └── test_task_store.py
```

## Running the Application

### Basic Usage

```bash
# Add a task
uv run python -m src add --title "Buy milk" --description "Get 2% milk"

# List all tasks
uv run python -m src list

# Mark task complete
uv run python -m src complete 1

# Delete a task
uv run python -m src delete 1
```

### Running Tests

```bash
uv run pytest tests/ -v
```

### Code Quality

```bash
# Type checking (if mypy is installed)
uv run mypy src/

# Linting (if ruff is installed)
uv run ruff check src/
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| In-memory storage | No persistence required by spec; session-only usage |
| Click framework | Standard, well-documented Python CLI library |
| Sequential IDs | Simple, predictable task identification |
| ISO 8601 timestamps | Standard format, human-readable |

## Troubleshooting

**Issue**: `ModuleNotFoundError`
**Solution**: Ensure UV has installed dependencies: `uv sync`

**Issue**: Command not found
**Solution**: Run with `uv run python -m src` or add `src` to PATH

---

**End of Quickstart Guide**
