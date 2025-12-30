# Todo CLI Application

A simple CLI todo application for task management.

## Installation

```bash
uv pip install -e .
```

## Usage

```bash
todo --help
todo add "Buy milk"
todo list
todo complete 1
todo delete 1
```

## Development

```bash
uv run pytest tests/ -v
```
