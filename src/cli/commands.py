"""CLI commands for the Todo CLI application using Click."""

import sys
from typing import Optional
from datetime import date, datetime

import click

from src.models.task import TaskStatus, TaskPriority, TaskCategory
from src.storage.task_store import TaskNotFoundError, TaskStore, TaskFilter, TaskSort, TaskSortBy, TaskSortOrder

# Global task store instance
task_store: Optional[TaskStore] = None


# Create or fetch the task store instance
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
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["high", "medium", "low"], case_sensitive=False),
    default="medium",
    help="Task priority (high/medium/low)",
)
@click.option(
    "--category",
    "-c",
    type=click.Choice(["work", "home"], case_sensitive=False),
    default=None,
    help="Task category (work/home)",
)
@click.option("--due-date", "-D", type=str, default=None, help="Task due date (YYYY-MM-DD format)")
def add(
    title: tuple, description: str, priority: str, category: Optional[str], due_date: Optional[str]
) -> None:
    """Add a new task to the todo list."""
    if not title:
        click.echo("Error: Task title cannot be empty", err=True)
        sys.exit(1)

    title_str = " ".join(title)
    if not title_str.strip():
        click.echo("Error: Task title cannot be empty", err=True)
        sys.exit(1)

    # Parse priority
    try:
        priority_enum = TaskPriority(priority.lower())
    except ValueError:
        click.echo("Error: Invalid priority. Must be high, medium, or low.", err=True)
        sys.exit(1)

    # Parse category (default to uncategorized if not provided)
    if category is None:
        category_enum = TaskCategory.UNCATEGORIZED
    else:
        try:
            category_enum = TaskCategory(category.lower())
        except ValueError:
            click.echo("Error: Invalid category. Must be work or home.", err=True)
            sys.exit(1)

    # Parse due date
    due_date_obj: Optional[date] = None
    if due_date:
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            click.echo("Error: Invalid date format. Use YYYY-MM-DD.", err=True)
            sys.exit(1)

    # Create and store the task
    store = get_task_store()
    task = store.add(
        title_str,
        description=description,
        priority=priority_enum,
        category=category_enum,
        due_date=due_date_obj,
    )
    click.echo(f"Added task {task.id}: {task.title}")


@main.command("list")
@click.option("--status", type=click.Choice(["pending", "completed"], case_sensitive=False), help="Filter by status")
@click.option("--priority", type=click.Choice(["high", "medium", "low"], case_sensitive=False), help="Filter by priority")
@click.option("--category", type=click.Choice(["work", "home"], case_sensitive=False), help="Filter by category")
@click.option("--due-date", "-D", type=str, default=None, help="Filter by due date (YYYY-MM-DD format)")
@click.option("--search", "-s", type=str, default=None, help="Search tasks by keyword (searches title and description)")
@click.option("--sort-by", type=click.Choice(["due_date", "priority", "title"], case_sensitive=False), help="Sort by field")
@click.option("--sort-order", type=click.Choice(["asc", "desc"], case_sensitive=False), default="asc", help="Sort order")
def list_tasks(
    status: Optional[str],
    priority: Optional[str],
    category: Optional[str],
    due_date: Optional[str],
    search: Optional[str],
    sort_by: Optional[str],
    sort_order: str,
) -> None:
    """List all tasks with optional filtering and sorting."""
    store = get_task_store()

    # Build filter
    task_filter = TaskFilter()
    if status:
        task_filter.status = TaskStatus.INCOMPLETE if status.lower() == "pending" else TaskStatus.COMPLETE
    if priority:
        task_filter.priority = TaskPriority(priority.lower())
    if category:
        task_filter.category = TaskCategory(category.lower())

    # Parse due date filter
    if due_date:
        try:
            task_filter.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            click.echo("Error: Invalid date format for --due-date. Use YYYY-MM-DD.", err=True)
            sys.exit(1)

    # Add keyword search
    if search:
        task_filter.keyword = search

    tasks = store.filter(task_filter)

    # Sort if requested
    if sort_by:
        sort_by_enum = TaskSortBy(sort_by.lower())
        sort_order_enum = TaskSortOrder.DESC if sort_order.lower() == "desc" else TaskSortOrder.ASC
        task_sort = TaskSort(by=sort_by_enum, order=sort_order_enum)
        tasks = store.sort(tasks, task_sort)

    if not tasks:
        click.echo("No tasks found. Add a task with: todo add 'Task name'")
        return

    # Calculate column widths
    id_width = max(len(str(t.id)) for t in tasks) + 2
    priority_width = max(len(t.priority.value) for t in tasks) + 2
    category_width = max(len(t.category.value) for t in tasks) + 2
    due_width = 12  # YYYY-MM-DD format
    title_width = max(len(t.title) for t in tasks)

    # Display header
    header = (
        f"{'ID':<{id_width}}| {'Status':<12}| {'Priority':<{priority_width}}| "
        f"{'Category':<{category_width}}| {'Due':<{due_width}}| Title"
    )
    click.echo(header)
    click.echo("-" * len(header))

    # Display tasks
    for task in tasks:
        status_marker = "[x]" if task.status == TaskStatus.COMPLETE else "[ ]"
        due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "-"
        click.echo(
            f"{task.id:<{id_width}}| {status_marker:<12}| {task.priority.value:<{priority_width}}| "
            f"{task.category.value:<{category_width}}| {due_str:<{due_width}}| {task.title}"
        )

    click.echo("Legend: [ ] = Incomplete  [x] = Complete")


@main.command("update")
@click.argument("task_id", type=int)
@click.option("--title", "-t", type=str, help="New task title")
@click.option("--description", "-d", type=str, help="New task description")
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["high", "medium", "low"], case_sensitive=False),
    help="New task priority",
)
@click.option(
    "--category",
    "-c",
    type=click.Choice(["work", "home"], case_sensitive=False),
    help="New task category",
)
@click.option("--due-date", "-D", type=str, default=None, help="New task due date (YYYY-MM-DD format, empty to clear)")
def update(
    task_id: int,
    title: Optional[str],
    description: Optional[str],
    priority: Optional[str],
    category: Optional[str],
    due_date: Optional[str],
) -> None:
    """Update an existing task."""
    store = get_task_store()

    # Parse optional fields
    priority_enum: Optional[TaskPriority] = None
    if priority:
        try:
            priority_enum = TaskPriority(priority.lower())
        except ValueError:
            click.echo("Error: Invalid priority. Must be high, medium, or low.", err=True)
            sys.exit(1)

    category_enum: Optional[TaskCategory] = None
    if category:
        try:
            category_enum = TaskCategory(category.lower())
        except ValueError:
            click.echo("Error: Invalid category. Must be work or home.", err=True)
            sys.exit(1)

    # Parse due date - None means don't change, empty string means clear
    due_date_obj: Optional[date] = None
    if due_date is not None:
        if due_date == "":
            due_date_obj = None  # Clear the due date
        else:
            try:
                due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
            except ValueError:
                click.echo("Error: Invalid date format. Use YYYY-MM-DD.", err=True)
                sys.exit(1)

    try:
        task = store.update(
            task_id,
            title=title,
            description=description,
            priority=priority_enum,
            category=category_enum,
            due_date=due_date_obj,
        )
        click.echo(f"Updated task {task.id}: {task.title}")
    except TaskNotFoundError:
        click.echo(f"Error: Task {task_id} not found.", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command("delete")
@click.argument("task_id", type=int)
def delete(task_id: int) -> None:
    """Delete a task from the todo list."""
    store = get_task_store()

    if store.delete(task_id):
        click.echo(f"Deleted task {task_id}.")
    else:
        click.echo(f"Error: Task {task_id} not found.", err=True)
        sys.exit(1)


@main.command("complete")
@click.argument("task_id", type=int)
def complete(task_id: int) -> None:
    """Mark a task as complete."""
    store = get_task_store()

    try:
        task = store.mark_complete(task_id)
        click.echo(f"Completed task {task.id}: {task.title}")
    except TaskNotFoundError:
        click.echo(f"Error: Task {task_id} not found.", err=True)
        sys.exit(1)


@main.command("incomplete")
@click.argument("task_id", type=int)
def incomplete(task_id: int) -> None:
    """Mark a task as incomplete (pending)."""
    store = get_task_store()

    try:
        task = store.mark_incomplete(task_id)
        click.echo(f"Marked task {task.id} as incomplete: {task.title}")
    except TaskNotFoundError:
        click.echo(f"Error: Task {task_id} not found.", err=True)
        sys.exit(1)


@main.command("menu")
def menu() -> None:
    """Launch the interactive menu system."""
    from src.cli.menu import main_menu_loop
    main_menu_loop()


if __name__ == "__main__":
    # If no command is provided, launch the interactive menu
    if len(sys.argv) == 1:
        from src.cli.menu import main_menu_loop
        main_menu_loop()
    else:
        main()
