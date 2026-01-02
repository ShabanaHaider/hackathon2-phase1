"""Interactive menu system for the Todo CLI application."""

import click
import os
import sys
from typing import Optional, List
from datetime import datetime, date, time


def clear_screen() -> None:
    """Clear the terminal screen in a platform-aware way."""
    if sys.platform.startswith('win'):
        os.system('cls')  # Windows
    else:
        os.system('clear')  # Unix/Linux/MacOS


from src.models.task import Task, TaskStatus, TaskPriority, TaskCategory
from src.storage.task_store import TaskStore, TaskFilter, TaskSort, TaskSortBy, TaskSortOrder
from src.cli.prompts import (
    prompt_for_title,
    prompt_for_description,
    prompt_for_priority,
    prompt_for_category,
    prompt_with_validation,
)
from src.cli.validation import (
    validate_due_date,
    validate_due_time,
    validate_task_id,
    validate_recurrence,
    validate_reminder_interval,
)
from src.cli.formatters import format_task_row, format_table_header
from src.models.recurrence import RecurrencePattern, RecurrenceInterval


def show_main_menu() -> int:
    """Display the main menu and get user selection.

    Returns:
        User's menu choice (1-7).
    """
    click.echo("\n" + "=" * 40)
    click.echo("  Todo Application - Main Menu")
    click.echo("=" * 40)
    click.echo("1. Add Task")
    click.echo("2. View Tasks")
    click.echo("3. Update Task")
    click.echo("4. Delete Task")
    click.echo("5. Complete Task")
    click.echo("6. Mark Incomplete")
    click.echo("7. Exit")
    click.echo("=" * 40)

    choice = click.prompt(
        "Select an option", type=click.IntRange(1, 7), default=1
    )
    return choice


def main_menu_loop() -> None:
    """Main menu loop with keyboard interrupt handling."""
    store = TaskStore()

    # Initialize and start reminder service
    from src.services.reminder_service import ReminderService
    reminder_service = ReminderService(store)
    reminder_service.start()

    # Refresh reminders initially
    reminder_service.refresh_reminders()

    try:
        while True:
            try:
                choice = show_main_menu()

                if choice == 1:
                    handle_add_task(store)
                    reminder_service.refresh_reminders()  # Refresh after adding task
                elif choice == 2:
                    # View Tasks with sub-options
                    handle_view_tasks(store)
                elif choice == 3:
                    # Update Task
                    handle_update_task(store)
                elif choice == 4:
                    # Delete Task
                    handle_delete_task(store)
                elif choice == 5:
                    # Complete Task
                    handle_complete_task(store)
                elif choice == 6:
                    # Mark Incomplete
                    handle_mark_incomplete_task(store)
                elif choice == 7:
                    click.echo("\nGoodbye!")
                    break

            except KeyboardInterrupt:
                if click.confirm(
                    "\n\nAre you sure you want to exit?", default=False
                ):
                    click.echo("\nGoodbye!")
                    break
                # Continue loop if user says no
    finally:
        # Ensure reminder service is stopped on exit
        reminder_service.stop()


def handle_mark_incomplete_task(store: TaskStore) -> None:
    """Handle marking a task as incomplete with task ID prompt."""
    click.echo("\n--- Mark Task Incomplete ---")

    # Prompt for task ID
    task_id_str = click.prompt("Enter task ID to mark as incomplete")
    try:
        task_id = int(task_id_str)
    except ValueError:
        click.echo(click.style(f"Invalid task ID: {task_id_str}", fg="red"))
        return

    # Verify task exists
    try:
        task = store.get(task_id)
        if task is None:
            click.echo(click.style(f"Task with ID {task_id} not found", fg="red"))
            return
    except Exception:
        click.echo(click.style(f"Task with ID {task_id} not found", fg="red"))
        return

    # Check if task is already incomplete
    if task.status == TaskStatus.INCOMPLETE:
        click.echo(click.style(f"Task {task_id} is already marked as incomplete", fg="yellow"))
        return

    try:
        incomplete_task = store.mark_incomplete(task_id)
        click.echo(click.style(f"[OK] Task {incomplete_task.id} marked as incomplete: {incomplete_task.title}", fg="green"))
    except Exception as e:
        click.echo(click.style(f"Error marking task as incomplete: {e}", fg="red"))


def display_tasks(tasks: List) -> None:
    """Display tasks in a formatted table."""
    if not tasks:
        click.echo("No tasks found.")
        return

    click.echo(format_table_header(tasks))
    for task in tasks:
        click.echo(format_task_row(task))


def handle_search_tasks(store: TaskStore) -> None:
    """Handle searching tasks by keyword."""
    click.echo("\n--- Search Tasks by Keyword ---")
    keyword = click.prompt("Enter keyword to search", default="", show_default=False)
    if keyword:
        task_filter = TaskFilter(keyword=keyword)
        tasks = store.filter(task_filter)
        display_tasks(tasks)
    else:
        click.echo("No keyword provided.")


def handle_view_pending_tasks(store: TaskStore) -> None:
    """Handle viewing pending tasks."""
    click.echo("\n--- View Pending Tasks ---")
    task_filter = TaskFilter(status=TaskStatus.INCOMPLETE)
    tasks = store.filter(task_filter)
    display_tasks(tasks)


def handle_view_completed_tasks(store: TaskStore) -> None:
    """Handle viewing completed tasks."""
    click.echo("\n--- View Completed Tasks ---")
    task_filter = TaskFilter(status=TaskStatus.COMPLETE)
    tasks = store.filter(task_filter)
    display_tasks(tasks)


def handle_view_tasks_by_priority(store: TaskStore) -> None:
    """Handle viewing tasks by priority."""
    click.echo("\n--- View Tasks by Priority ---")
    priority_choice = click.prompt(
        "Filter by priority (high/medium/low)",
        type=click.Choice(["high", "medium", "low"], case_sensitive=False),
        default="medium"
    )
    priority = TaskPriority(priority_choice)
    task_filter = TaskFilter(priority=priority)
    tasks = store.filter(task_filter)
    display_tasks(tasks)


def handle_view_tasks_by_due_date(store: TaskStore) -> None:
    """Handle viewing tasks by due date with improved user experience."""
    click.echo("\n--- View Tasks by Due Date ---")

    # Give user more explicit instructions
    click.echo("Choose a due date filter option:")
    click.echo("  - 'overdue': tasks past their due date")
    click.echo("  - 'today': tasks due today")
    click.echo("  - 'this_week': tasks due within the next 7 days")
    click.echo("  - 'future': tasks due after today")
    click.echo("  - 'none': tasks without a due date")
    click.echo("  - 'due_date': tasks with a specific due date")

    date_choice = click.prompt(
        "Filter by due date (overdue/today/this_week/future/none/due_date)",
        type=click.Choice(["overdue", "today", "this_week", "future", "none", "due_date"], case_sensitive=False),
        default="today"
    )

    # Get all tasks initially
    tasks = store.get_all()

    if date_choice == "overdue":
        tasks = [task for task in tasks if task.is_overdue()]
    elif date_choice == "today":
        from datetime import date
        today = date.today()
        tasks = [task for task in tasks if task.due_date == today]
    elif date_choice == "this_week":
        from datetime import date, timedelta
        today = date.today()
        week_from_now = today + timedelta(days=7)
        tasks = [task for task in tasks if task.due_date and today <= task.due_date <= week_from_now]
    elif date_choice == "future":
        from datetime import date
        today = date.today()
        tasks = [task for task in tasks if task.due_date and task.due_date > today]
    elif date_choice == "none":
        tasks = [task for task in tasks if task.due_date is None]
    elif date_choice == "due_date":
        from datetime import date
        due_date_str = click.prompt("Enter due date (YYYY-MM-DD)", type=str)
        try:
            due_date = date.fromisoformat(due_date_str)
            tasks = [task for task in tasks if task.due_date == due_date]
        except ValueError:
            click.echo(click.style(f"Invalid date format: {due_date_str}. Please use YYYY-MM-DD format.", fg="red"))
            return

    display_tasks(tasks)


def handle_sort_tasks_by_due_date(store: TaskStore) -> None:
    """Handle sorting tasks by due date."""
    click.echo("\n--- Sort Tasks by Due Date ---")
    tasks = store.get_all()
    # Sort overdue tasks first, then by due date ascending
    tasks.sort(key=lambda t: (not t.is_overdue(), t.get_full_due_datetime() or datetime.max))
    display_tasks(tasks)


def handle_sort_tasks_by_priority(store: TaskStore) -> None:
    """Handle sorting tasks by priority."""
    click.echo("\n--- Sort Tasks by Priority ---")
    tasks = store.get_all()
    priority_order = {TaskPriority.HIGH: 0, TaskPriority.MEDIUM: 1, TaskPriority.LOW: 2}
    tasks.sort(key=lambda t: priority_order.get(t.priority, 3))
    display_tasks(tasks)


def handle_sort_tasks_alphabetically(store: TaskStore) -> None:
    """Handle sorting tasks alphabetically."""
    click.echo("\n--- Sort Tasks Alphabetically ---")
    tasks = store.get_all()
    tasks.sort(key=lambda t: t.title.lower())
    display_tasks(tasks)


def handle_view_recurring_tasks(store: TaskStore) -> None:
    """Handle viewing recurring tasks."""
    click.echo("\n--- View Recurring Tasks ---")
    tasks = store.get_all()
    tasks = [task for task in tasks if task.recurrence is not None]
    display_tasks(tasks)


def handle_view_overdue_tasks(store: TaskStore) -> None:
    """Handle viewing overdue tasks."""
    click.echo("\n--- View Overdue Tasks ---")
    tasks = store.get_all()
    tasks = [task for task in tasks if task.is_overdue()]
    display_tasks(tasks)


def handle_add_task(store: TaskStore) -> None:
    """Handle adding a new task with guided prompts."""
    click.echo("\n--- Add New Task ---")

    # Prompt for required title
    title = prompt_for_title()
    if title is None:
        return  # Cancelled by user

    # Prompt for optional description
    description = prompt_for_description()
    if description is None:  # If validation failed completely
        description = ""

    # Prompt for priority
    priority_str = prompt_for_priority()
    if priority_str is None:
        priority = TaskPriority.MEDIUM
    else:
        priority = TaskPriority(priority_str)

    # Prompt for category
    category_str = prompt_for_category()
    if category_str is None:
        category = TaskCategory.UNCATEGORIZED
    else:
        category = TaskCategory(category_str)

    # Prompt for due date
    due_date_str = click.prompt("Task due date (YYYY-MM-DD, press Enter to skip)", default="", show_default=False)
    if due_date_str:
        try:
            due_date = validate_due_date(due_date_str)
        except Exception:
            click.echo(click.style(f"Invalid date format: {due_date_str}. Task will be created without due date.", fg="yellow"))
            due_date = None
    else:
        due_date = None

    # Prompt for due time (only if due date is set)
    due_time = None
    if due_date:
        due_time_str = click.prompt("Task due time (HH:MM, press Enter to skip)", default="", show_default=False)
        if due_time_str:
            try:
                from src.cli.validation import validate_due_time
                due_time = validate_due_time(due_time_str)
            except Exception:
                click.echo(click.style(f"Invalid time format: {due_time_str}. Task will be created without due time.", fg="yellow"))
    else:
        # If no due date, don't allow due time
        due_time = None

    # Prompt for recurrence
    recurrence_str = click.prompt("Task recurrence (daily/weekly/monthly/custom/press Enter to skip)", default="", show_default=False)
    recurrence = None
    if recurrence_str:
        try:
            recurrence_type = validate_recurrence(recurrence_str)
            if recurrence_type:
                interval_type = RecurrenceInterval(recurrence_type)
                interval_value = 1

                # If custom recurrence, ask for interval value
                if interval_type == RecurrenceInterval.CUSTOM:
                    interval_value = int(click.prompt("Recurrence interval (days)", default=1, type=int))
                    if interval_value <= 0:
                        click.echo(click.style("Invalid interval value. Task will be created without recurrence.", fg="yellow"))
                        recurrence = None
                    else:
                        recurrence = RecurrencePattern(
                            interval_type=interval_type,
                            interval_value=interval_value
                        )
                else:
                    recurrence = RecurrencePattern(
                        interval_type=interval_type,
                        interval_value=interval_value
                    )
        except Exception:
            click.echo(click.style(f"Invalid recurrence: {recurrence_str}. Task will be created without recurrence.", fg="yellow"))

    # Prompt for reminder intervals (only if due date is set)
    reminder_intervals = []
    if due_date:
        add_reminders = click.confirm("Would you like to add reminders?", default=False)
        if add_reminders:
            while True:
                reminder_str = click.prompt("Reminder interval in minutes before due time (or 'done' to finish)", default="done", show_default=False)
                if reminder_str.lower() == 'done':
                    break
                try:
                    interval = validate_reminder_interval(reminder_str)
                    reminder_intervals.append(interval)

                    if len(reminder_intervals) >= 5:
                        click.echo("Maximum 5 reminders per task reached.")
                        break

                    add_another = click.confirm("Add another reminder?", default=False)
                    if not add_another:
                        break
                except Exception as e:
                    click.echo(click.style(f"Invalid reminder interval: {reminder_str}. {str(e)}", fg="red"))

    # Create task
    task = store.add(
        title=title,
        description=description,
        priority=priority,
        category=category,
        due_date=due_date
    )

    # Update additional fields after task creation
    if due_time:
        task.due_time = due_time
    if recurrence:
        task.recurrence = recurrence
    if reminder_intervals:
        task.reminder_intervals = reminder_intervals
    task.updated_at = datetime.now()

    click.echo(click.style(f"\n[OK] Task created successfully", fg="green"))
    click.echo(f"  ID: {task.id}")
    click.echo(f"  Title: {task.title}")
    if task.due_date:
        due_str = f"{task.due_date}" + (f" {task.due_time}" if task.due_time else "")
        click.echo(f"  Due: {due_str}")
    if task.recurrence:
        click.echo(f"  Recurrence: {task.recurrence}")
    if task.reminder_intervals:
        intervals_str = ", ".join([f"{interval}min" for interval in task.reminder_intervals])
        click.echo(f"  Reminders: {intervals_str}")


def handle_view_tasks(store: TaskStore) -> None:
    """Handle viewing tasks with interactive sub-options for filtering and sorting."""
    click.echo("\n--- View Tasks ---")
    click.echo("1. View All Tasks")
    click.echo("2. Search by Keyword")
    click.echo("3. Filter by Status")
    click.echo("4. Filter by Priority")
    click.echo("5. Filter by Due Date")
    click.echo("6. Sort by Due Date")
    click.echo("7. Sort by Priority")
    click.echo("8. Sort Alphabetically")
    click.echo("9. Show Only Recurring Tasks")
    click.echo("10. Show Only Overdue Tasks")
    click.echo("11. Show Only Tasks Due Today")
    click.echo("12. Show Only Tasks Due This Week")
    click.echo("13. Go to Main Menu")
    click.echo("=" * 40)

    choice = click.prompt(
        "Select an option", type=click.IntRange(1, 13), default=1
    )

    # Get all tasks initially
    tasks = store.get_all()

    if choice == 1:
        # View All Tasks - no filtering
        pass
    elif choice == 2:
        # Search by Keyword
        keyword = click.prompt("Enter keyword to search", default="", show_default=False)
        if keyword:
            task_filter = TaskFilter(keyword=keyword)
            tasks = store.filter(task_filter)
    elif choice == 3:
        # Filter by Status
        status_choice = click.prompt(
            "Filter by status (pending/completed)",
            type=click.Choice(["pending", "completed"], case_sensitive=False),
            default="pending"
        )
        status = TaskStatus.INCOMPLETE if status_choice == "pending" else TaskStatus.COMPLETE
        task_filter = TaskFilter(status=status)
        tasks = store.filter(task_filter)
    elif choice == 4:
        # Filter by Priority
        priority_choice = click.prompt(
            "Filter by priority (high/medium/low)",
            type=click.Choice(["high", "medium", "low"], case_sensitive=False),
            default="medium"
        )
        priority = TaskPriority(priority_choice)
        task_filter = TaskFilter(priority=priority)
        tasks = store.filter(task_filter)
    elif choice == 5:
        # Filter by Due Date - with improved user experience
        click.echo("\nChoose a due date filter option:")
        click.echo("  - 'overdue': tasks past their due date")
        click.echo("  - 'today': tasks due today")
        click.echo("  - 'this_week': tasks due within the next 7 days")
        click.echo("  - 'future': tasks due after today")
        click.echo("  - 'none': tasks without a due date")
        click.echo("  - 'due_date': tasks with a specific due date (you'll enter the date after selecting this option)")
        click.echo("")

        date_choice = click.prompt(
            "Filter by due date (overdue/today/this_week/future/none/due_date)",
            type=click.Choice(["overdue", "today", "this_week", "future", "none", "due_date"], case_sensitive=False),
            default="today"
        )

        if date_choice == "overdue":
            tasks = [task for task in tasks if task.is_overdue()]
        elif date_choice == "today":
            from datetime import date
            today = date.today()
            tasks = [task for task in tasks if task.due_date == today]
        elif date_choice == "this_week":
            from datetime import date, timedelta
            today = date.today()
            week_from_now = today + timedelta(days=7)
            tasks = [task for task in tasks if task.due_date and today <= task.due_date <= week_from_now]
        elif date_choice == "future":
            from datetime import date
            today = date.today()
            tasks = [task for task in tasks if task.due_date and task.due_date > today]
        elif date_choice == "none":
            tasks = [task for task in tasks if task.due_date is None]
        elif date_choice == "due_date":
            from datetime import date
            due_date_str = click.prompt("Enter due date (YYYY-MM-DD)", type=str)
            try:
                due_date = date.fromisoformat(due_date_str)
                tasks = [task for task in tasks if task.due_date == due_date]
            except ValueError:
                click.echo(click.style(f"Invalid date format: {due_date_str}. Please use YYYY-MM-DD format.", fg="red"))
                return
    elif choice == 6:
        # Sort by Due Date
        # Sort overdue tasks first, then by due date ascending
        tasks.sort(key=lambda t: (not t.is_overdue(), t.get_full_due_datetime() or datetime.max))
    elif choice == 7:
        # Sort by Priority
        priority_order = {TaskPriority.HIGH: 0, TaskPriority.MEDIUM: 1, TaskPriority.LOW: 2}
        tasks.sort(key=lambda t: priority_order.get(t.priority, 3))
    elif choice == 8:
        # Sort Alphabetically
        tasks.sort(key=lambda t: t.title.lower())
    elif choice == 9:
        # Show Only Recurring Tasks
        tasks = [task for task in tasks if task.recurrence is not None]
    elif choice == 10:
        # Show Only Overdue Tasks
        tasks = [task for task in tasks if task.is_overdue()]
    elif choice == 11:
        # Show Only Tasks Due Today
        from datetime import date
        today = date.today()
        tasks = [task for task in tasks if task.due_date == today]
    elif choice == 12:
        # Show Only Tasks Due This Week
        from datetime import date, timedelta
        today = date.today()
        week_from_now = today + timedelta(days=7)
        tasks = [task for task in tasks if task.due_date and today <= task.due_date <= week_from_now]
    elif choice == 13:
        # Go to Main Menu - just return to exit this function and go back to main menu
        return

    if choice != 13:  # Only display tasks if not choosing to go to main menu
        if not tasks:
            click.echo("No tasks found.")
            return

        # Display tasks in a formatted table
        click.echo(format_table_header(tasks))
        for task in tasks:
            click.echo(format_task_row(task))


def handle_update_task(store: TaskStore) -> None:
    """Handle updating a task with task ID prompt and field selection."""
    click.echo("\n--- Update Task ---")

    # Prompt for task ID
    task_id_str = click.prompt("Enter task ID to update")
    try:
        task_id = int(task_id_str)
    except ValueError:
        click.echo(click.style(f"Invalid task ID: {task_id_str}", fg="red"))
        return

    # Verify task exists
    try:
        task = store.get(task_id)
        if task is None:
            click.echo(click.style(f"Task with ID {task_id} not found", fg="red"))
            return
    except Exception:
        click.echo(click.style(f"Task with ID {task_id} not found", fg="red"))
        return

    click.echo(f"Updating task: {task.title}")

    # Prompt for which field to update
    fields = ["title", "description", "priority", "category", "due_date", "due_time", "recurrence", "reminders"]
    update_field = click.prompt(
        "Which field would you like to update?",
        type=click.Choice(fields, case_sensitive=False),
        default="title"
    )

    # Update the selected field
    try:
        if update_field == "title":
            new_title = prompt_for_title()
            if new_title is not None:
                store.update(task_id, title=new_title)
                click.echo(click.style(f"[OK] Title updated", fg="green"))

        elif update_field == "description":
            new_description = prompt_for_description()
            if new_description is not None:
                store.update(task_id, description=new_description)
                click.echo(click.style(f"[OK] Description updated", fg="green"))

        elif update_field == "priority":
            new_priority_str = prompt_for_priority()
            if new_priority_str is not None:
                new_priority = TaskPriority(new_priority_str)
                store.update(task_id, priority=new_priority)
                click.echo(click.style(f"[OK] Priority updated", fg="green"))

        elif update_field == "category":
            new_category_str = prompt_for_category()
            if new_category_str is not None:
                new_category = TaskCategory(new_category_str)
                store.update(task_id, category=new_category)
                click.echo(click.style(f"[OK] Category updated", fg="green"))

        elif update_field == "due_date":
            due_date_str = click.prompt("New due date (YYYY-MM-DD, press Enter to clear)", default="", show_default=False)
            if due_date_str:
                try:
                    new_due_date = validate_due_date(due_date_str)
                    store.update(task_id, due_date=new_due_date)
                    click.echo(click.style(f"[OK] Due date updated", fg="green"))
                except Exception as e:
                    click.echo(click.style(f"Invalid date format: {due_date_str}", fg="red"))
            else:
                # Clear due date
                store.update(task_id, due_date=None)
                click.echo(click.style(f"[OK] Due date cleared", fg="green"))

        elif update_field == "due_time":
            # Update due time
            due_time_str = click.prompt("New due time (HH:MM, press Enter to clear)", default="", show_default=False)
            if due_time_str:
                try:
                    from src.cli.validation import validate_due_time
                    new_due_time = validate_due_time(due_time_str)
                    # Update the task directly since the store doesn't have a due_time update method
                    task = store.get(task_id)
                    if task:
                        task.due_time = new_due_time
                        task.updated_at = datetime.now()
                        click.echo(click.style(f"[OK] Due time updated", fg="green"))
                except Exception as e:
                    click.echo(click.style(f"Invalid time format: {due_time_str}", fg="red"))
            else:
                # Clear due time
                task = store.get(task_id)
                if task:
                    task.due_time = None
                    task.updated_at = datetime.now()
                    click.echo(click.style(f"[OK] Due time cleared", fg="green"))

        elif update_field == "recurrence":
            # Update recurrence
            recurrence_str = click.prompt("New recurrence (daily/weekly/monthly/custom/press Enter to clear)", default="", show_default=False)
            if recurrence_str:
                try:
                    recurrence_type = validate_recurrence(recurrence_str)
                    if recurrence_type:
                        interval_type = RecurrenceInterval(recurrence_type)
                        interval_value = 1

                        # If custom recurrence, ask for interval value
                        if interval_type == RecurrenceInterval.CUSTOM:
                            interval_value = int(click.prompt("Recurrence interval (days)", default=1, type=int))
                            if interval_value <= 0:
                                raise ValueError("Invalid interval value")

                        recurrence = RecurrencePattern(
                            interval_type=interval_type,
                            interval_value=interval_value
                        )
                        # Update the task directly since the store doesn't have a recurrence update method
                        task = store.get(task_id)
                        if task:
                            task.recurrence = recurrence
                            task.updated_at = datetime.now()
                            click.echo(click.style(f"[OK] Recurrence updated", fg="green"))
                except Exception as e:
                    click.echo(click.style(f"Invalid recurrence: {recurrence_str}", fg="red"))
            else:
                # Clear recurrence
                task = store.get(task_id)
                if task:
                    task.recurrence = None
                    task.updated_at = datetime.now()
                    click.echo(click.style(f"[OK] Recurrence cleared", fg="green"))

        elif update_field == "reminders":
            # Update reminders
            add_reminders = click.confirm("Would you like to set new reminders? (Press Enter to clear existing)", default=False)
            if add_reminders:
                reminder_intervals = []
                while True:
                    reminder_str = click.prompt("Reminder interval in minutes before due time (or 'done' to finish)", default="done", show_default=False)
                    if reminder_str.lower() == 'done':
                        break
                    try:
                        interval = validate_reminder_interval(reminder_str)
                        reminder_intervals.append(interval)

                        if len(reminder_intervals) >= 5:
                            click.echo("Maximum 5 reminders per task reached.")
                            break

                        add_another = click.confirm("Add another reminder?", default=False)
                        if not add_another:
                            break
                    except Exception as e:
                        click.echo(click.style(f"Invalid reminder interval: {reminder_str}. {str(e)}", fg="red"))

                # Update the task directly since the store doesn't have a reminder update method
                task = store.get(task_id)
                if task:
                    task.reminder_intervals = reminder_intervals
                    task.updated_at = datetime.now()
                    if reminder_intervals:
                        intervals_str = ", ".join([f"{interval}min" for interval in reminder_intervals])
                        click.echo(click.style(f"[OK] Reminders updated: {intervals_str}", fg="green"))
                    else:
                        click.echo(click.style(f"[OK] All reminders cleared", fg="green"))
            else:
                # Clear all reminders
                task = store.get(task_id)
                if task:
                    task.reminder_intervals = []
                    task.updated_at = datetime.now()
                    click.echo(click.style(f"[OK] All reminders cleared", fg="green"))

    except Exception as e:
        click.echo(click.style(f"Error updating task: {e}", fg="red"))


def handle_delete_task(store: TaskStore) -> None:
    """Handle deleting a task with task ID prompt and confirmation."""
    click.echo("\n--- Delete Task ---")

    # Prompt for task ID
    task_id_str = click.prompt("Enter task ID to delete")
    try:
        task_id = int(task_id_str)
    except ValueError:
        click.echo(click.style(f"Invalid task ID: {task_id_str}", fg="red"))
        return

    # Verify task exists
    try:
        task = store.get(task_id)
        if task is None:
            click.echo(click.style(f"Task with ID {task_id} not found", fg="red"))
            return
    except Exception:
        click.echo(click.style(f"Task with ID {task_id} not found", fg="red"))
        return

    click.echo(f"Task to delete: {task.title}")

    # Check if task is recurring
    if task.recurrence:
        click.echo(click.style("Note: This is a recurring task. Only this instance will be deleted.", fg="yellow"))
        click.echo("Future instances remain scheduled.")

    # Confirm deletion
    if click.confirm("Are you sure you want to delete this task?", default=False):
        if store.delete(task_id):
            click.echo(click.style(f"[OK] Task {task_id} deleted", fg="green"))
        else:
            click.echo(click.style(f"Error deleting task {task_id}", fg="red"))
    else:
        click.echo("Deletion cancelled.")


def handle_complete_task(store: TaskStore) -> None:
    """Handle completing a task with task ID prompt."""
    click.echo("\n--- Complete Task ---")

    # Prompt for task ID
    task_id_str = click.prompt("Enter task ID to complete")
    try:
        task_id = int(task_id_str)
    except ValueError:
        click.echo(click.style(f"Invalid task ID: {task_id_str}", fg="red"))
        return

    # Verify task exists
    try:
        task = store.get(task_id)
        if task is None:
            click.echo(click.style(f"Task with ID {task_id} not found", fg="red"))
            return
    except Exception:
        click.echo(click.style(f"Task with ID {task_id} not found", fg="red"))
        return

    # Check if task is already complete
    if task.status == TaskStatus.COMPLETE:
        click.echo(click.style(f"Task {task_id} is already marked as complete", fg="yellow"))
        return

    try:
        completed_task = store.mark_complete(task_id)
        click.echo(click.style(f"[OK] Task {completed_task.id} marked as complete: {completed_task.title}", fg="green"))

        # Check if task is recurring and create next instance if needed
        if completed_task.recurrence:
            from src.services.recurrence_service import RecurrenceService
            recurrence_service = RecurrenceService()
            next_instance = recurrence_service.create_next_instance(completed_task, store)

            click.echo(click.style(f"[NEXT] Next instance created", fg="green"))
            click.echo(f"  ID: {next_instance.id}")
            click.echo(f"  Title: {next_instance.title}")
            if next_instance.due_date:
                due_str = f"{next_instance.due_date}" + (f" {next_instance.due_time}" if next_instance.due_time else "")
                click.echo(f"  Due: {due_str} (in {(next_instance.get_full_due_datetime() - datetime.now()).days + 1} days)")
            click.echo(f"  Recurrence: {next_instance.recurrence}")

    except Exception as e:
        click.echo(click.style(f"Error completing task: {e}", fg="red"))
