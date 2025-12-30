"""CLI commands for the Todo CLI application using Click."""

import sys
from typing import Optional

import click

from src.models.task import TaskStatus
from src.storage.task_store import TaskNotFoundError, TaskStore


# Global task store instance
task_store: Optional[TaskStore] = None


def get_task_store() -> TaskStore:
    """Get or create the global task store instance."""
    global task_store
    if task_store is None:
        task_store = TaskStore()
    return task_store


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """A simple CLI todo application for task management."""
    pass


@main.command("add")
@click.argument("title", type=str, nargs=-1)
@click.option("--description", "-d", default="", type=str, help="Task description")
def add(title: tuple, description: str) -> None:
    """Add a new task to the todo list.

    \b
    Examples:
      todo add "Buy milk"
      todo add "Buy milk" --description "Get 2% milk from store"
      todo add --title "Buy milk" --description "Get 2% milk"
    """
    if not title:
        click.echo("Error: Task title cannot be empty", err=True)
        sys.exit(1)

    title_str = " ".join(title)
    if not title_str.strip():
        click.echo("Error: Task title cannot be empty", err=True)
        sys.exit(1)

    if len(title_str) > 255:
        click.echo("Error: Title exceeds 255 characters", err=True)
        sys.exit(1)

    if len(description) > 2000:
        click.echo("Error: Description exceeds 2000 characters", err=True)
        sys.exit(1)

    store = get_task_store()
    task = store.add(title_str, description)
    click.echo(f"Added task {task.id}: {task.title}")


@main.command("list")
def list_tasks() -> None:
    """List all tasks with their completion status.

    \b
    Examples:
      todo list
    """
    store = get_task_store()
    tasks = store.get_all()

    if not tasks:
        click.echo("No tasks found. Add a task with: todo add --title \"Task name\"")
        return

    # Calculate column widths
    id_width = max(len(str(t.id)) for t in tasks) + 2
    title_width = max(len(t.title) for t in tasks)
    desc_width = max(len(t.description) for t in tasks)

    # Build header
    header = f"{'ID':<{id_width}}| {'Status':<12}| {'Title':<{title_width}}| Description"
    click.echo(header)
    click.echo("-" * len(header))

    # Build rows
    for task in tasks:
        status_marker = "[x]" if task.status == TaskStatus.COMPLETE else "[ ]"
        title_display = task.title[:title_width] if len(task.title) <= title_width else task.title[:title_width-3] + "..."
        desc_display = task.description[:desc_width] if len(task.description) <= desc_width else task.description[:desc_width-3] + "..."
        row = f"{task.id:<{id_width}}| {status_marker:<12}| {title_display:<{title_width}}| {desc_display}"
        click.echo(row)

    click.echo("")
    click.echo("Legend: [ ] = Incomplete  [x] = Complete")


@main.command("update")
@click.argument("task_id", type=int)
@click.option("--title", "-t", type=str, help="New task title")
@click.option("--description", "-d", type=str, help="New task description")
def update(task_id: int, title: Optional[str], description: Optional[str]) -> None:
    """Update an existing task.

    \b
    Examples:
      todo update 1 --title "New title"
      todo update 1 --description "New description"
      todo update 1 --title "New title" --description "New description"
    """
    store = get_task_store()

    try:
        task = store.update(task_id, title=title, description=description)
        if title and description:
            click.echo(f"Updated task {task.id}: {task.title}")
        elif title:
            click.echo(f"Updated task {task.id}: {task.title}")
        else:
            click.echo(f"Updated task {task.id} description")
    except TaskNotFoundError:
        click.echo(f"Error: Task {task_id} not found", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command("delete")
@click.argument("task_id", type=int)
def delete(task_id: int) -> None:
    """Delete a task by ID.

    \b
    Examples:
      todo delete 1
    """
    store = get_task_store()

    if store.delete(task_id):
        click.echo(f"Deleted task {task_id}")
    else:
        click.echo(f"Error: Task {task_id} not found", err=True)
        sys.exit(1)


@main.command("complete")
@click.argument("task_id", type=int)
def complete(task_id: int) -> None:
    """Mark a task as complete.

    \b
    Examples:
      todo complete 1
    """
    store = get_task_store()

    try:
        task = store.mark_complete(task_id)
        click.echo(f"Marked task {task.id} as complete")
    except TaskNotFoundError:
        click.echo(f"Error: Task {task_id} not found", err=True)
        sys.exit(1)


@main.command("incomplete")
@click.argument("task_id", type=int)
def incomplete(task_id: int) -> None:
    """Mark a task as incomplete.

    \b
    Examples:
      todo incomplete 1
    """
    store = get_task_store()

    try:
        task = store.mark_incomplete(task_id)
        click.echo(f"Marked task {task.id} as incomplete")
    except TaskNotFoundError:
        click.echo(f"Error: Task {task_id} not found", err=True)
        sys.exit(1)
