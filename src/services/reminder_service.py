"""Reminder service for background notification checking."""

import heapq
import threading
import time
from datetime import datetime
from typing import TYPE_CHECKING, List

from src.models.reminder import Reminder

if TYPE_CHECKING:
    from src.models.task import Task
    from src.storage.task_store import TaskStore


class ReminderService:
    """Background service that checks for due reminders and sends notifications.

    This service runs a daemon thread that polls every 10 seconds for reminders
    that are due and sends desktop notifications.
    """

    def __init__(self, task_store: "TaskStore"):
        """Initialize the reminder service.

        Args:
            task_store: TaskStore instance to access tasks.
        """
        self.task_store = task_store
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.reminders: List[Reminder] = []
        self.thread = threading.Thread(target=self._check_reminders, daemon=True)

    def start(self) -> None:
        """Start the reminder checking thread."""
        if not self.thread.is_alive():
            self.thread.start()

    def stop(self) -> None:
        """Stop the reminder thread gracefully."""
        self.stop_event.set()
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)

    def refresh_reminders(self) -> None:
        """Rebuild reminder queue from current tasks.

        This should be called whenever tasks are added, updated, or deleted.
        """
        # Get tasks outside the lock to minimize lock time
        tasks = self.task_store.get_all()

        with self.lock:
            self.reminders = []

            for task in tasks:
                if task.status == task.status.COMPLETE or not task.reminder_intervals:
                    continue

                reminder_times = task.calculate_reminder_times()
                for reminder_time in reminder_times:
                    # Calculate the minutes before based on the reminder time
                    due_dt = task.get_full_due_datetime()
                    if due_dt:
                        minutes_before = int((due_dt - reminder_time).total_seconds() / 60)
                    else:
                        minutes_before = 0

                    reminder = Reminder(
                        task_id=task.id,
                        reminder_time=reminder_time,
                        minutes_before=minutes_before
                    )
                    heapq.heappush(self.reminders, reminder)

    def _check_reminders(self) -> None:
        """Background loop that checks for due reminders.

        Runs in daemon thread, polls every 10 seconds.
        """
        while not self.stop_event.is_set():
            try:
                # Check for due reminders
                current_time = datetime.now()
                due_reminders = []

                with self.lock:
                    # Get all reminders that are due
                    temp_reminders = []
                    while self.reminders:
                        reminder = heapq.heappop(self.reminders)
                        if reminder.is_due():
                            due_reminders.append(reminder)
                        else:
                            temp_reminders.append(reminder)

                    # Put back the non-due reminders
                    self.reminders = temp_reminders
                    heapq.heapify(self.reminders)

                # Send notifications for due reminders
                for reminder in due_reminders:
                    with self.lock:  # Thread-safe access to task_store
                        task = self.task_store.get(reminder.task_id)
                    if task:
                        self._send_notification(task, reminder.minutes_before)
                        reminder.mark_sent()

                # Sleep for 10 seconds before next check
                time.sleep(10)
            except Exception as e:
                # In a real implementation, we'd log this error
                time.sleep(10)  # Continue polling even if there's an error

    def _send_notification(self, task: "Task", minutes_before: int) -> None:
        """Send desktop notification for a reminder.

        Args:
            task: The task to send notification for.
            minutes_before: How many minutes before due time.
        """
        try:
            # Try to import plyer for desktop notifications
            from plyer import notification
            due_dt = task.get_full_due_datetime()
            due_str = due_dt.strftime("%Y-%m-%d %H:%M") if due_dt else "Unknown"
            notification.notify(
                title="Todo Reminder",
                message=f"Task: {task.title}\nDue: {due_str}\nTime remaining: {minutes_before} minutes",
                timeout=10
            )
        except ImportError:
            # Fallback to console notification if plyer is not available
            print(f"[REMINDER] {task.title} (due in {minutes_before} minutes at {task.get_full_due_datetime()})")
        except Exception:
            # If notification fails for any reason, fallback to console
            print(f"[REMINDER] {task.title} (due soon)")
