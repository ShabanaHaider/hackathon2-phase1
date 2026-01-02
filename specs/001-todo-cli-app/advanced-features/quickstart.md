# Quickstart Guide: Advanced Task Features

**Feature**: Recurring Tasks and Due Date Reminders
**Version**: 1.0.0
**Date**: 2026-01-01

---

## Overview

This guide will help you get started with the advanced task management features:
- **Due dates with specific times**: Set precise deadlines for your tasks
- **Reminders**: Get desktop notifications before tasks are due
- **Recurring tasks**: Automate repetitive tasks that repeat daily, weekly, monthly, or at custom intervals

---

## Prerequisites

- Todo CLI application installed (`uv pip install -e .`)
- Desktop notification support (automatic on Windows, macOS, Linux)
- Python 3.13+

---

## Quick Start Examples

### 1. Setting Due Dates and Times

**Basic due date** (no specific time):
```bash
todo add "Submit report" --due 2026-01-15
```
*Task is due anytime on January 15, 2026*

**Due date with specific time**:
```bash
todo add "Team meeting" --due 2026-01-10 --due-time 14:00
```
*Task is due on January 10, 2026 at 2:00 PM*

**View tasks with due dates**:
```bash
todo list --sort-by-due
```
*Shows all tasks sorted by due date (overdue tasks appear first)*

---

### 2. Setting Up Reminders

**Single reminder** (15 minutes before):
```bash
todo add "Doctor appointment" --due 2026-01-08 --due-time 10:00 --remind-before 15
```
*You'll receive a desktop notification at 9:45 AM*

**Multiple reminders**:
```bash
todo add "Project deadline" --due 2026-01-20 --due-time 17:00 \
  --remind-before 1440 \
  --remind-before 60 \
  --remind-before 15
```
*Reminders at: 1 day before (1440 min), 1 hour before (60 min), and 15 minutes before*

**What you'll see**:
When a reminder is due, you'll get a desktop notification:
```
─────────────────────────
  Todo Reminder
─────────────────────────
Task: "Doctor appointment"
Due: 2026-01-08 10:00
Time remaining: 15 minutes
─────────────────────────
```

**Important Notes**:
- Reminders only work while the todo app has a background process running
- Maximum 5 reminders per task
- Notifications appear in your system notification center/tray

---

### 3. Creating Recurring Tasks

**Daily recurring task**:
```bash
todo add "Daily standup" --due 2026-01-02 --due-time 09:00 --recurrence daily
```
*Repeats every day at 9:00 AM*

**Weekly recurring task**:
```bash
todo add "Team meeting" --due 2026-01-03 --due-time 14:00 --recurrence weekly
```
*Repeats every Friday (7 days) at 2:00 PM*

**Monthly recurring task**:
```bash
todo add "Monthly report" --due 2026-01-31 --due-time 17:00 --recurrence monthly
```
*Repeats every 30 days at 5:00 PM*

**Custom interval** (every 3 days):
```bash
todo add "Water plants" --recurrence custom --recurrence-days 3
```
*Repeats every 3 days*

---

### 4. Working with Recurring Tasks

**Completing a recurring task**:
```bash
$ todo complete 5
✓ Task marked as complete
  ID: 5
  Title: "Weekly meeting"

↻ Next instance created
  ID: 12
  Title: "Weekly meeting"
  Due: 2026-01-10 14:00 (in 7 days)
  Recurrence: Weekly
```
*Automatically creates the next instance 7 days from now*

**Deleting a recurring task instance**:
```bash
$ todo delete 5
✓ Current instance deleted
  ID: 5
  Title: "Weekly meeting"

Note: This is a recurring task. Only this instance was deleted.
      Future instances remain scheduled.
```
*Only deletes this occurrence - future instances remain*

**Viewing recurring tasks**:
```bash
todo list --recurring-only
```
*Shows only tasks with recurrence patterns*

---

### 5. Combining Features

**Recurring task with reminders**:
```bash
todo add "Submit timesheet" \
  --due 2026-01-05 \
  --due-time 17:00 \
  --recurrence weekly \
  --remind-before 60 \
  --remind-before 15 \
  --category work \
  --priority high
```
*Every Friday at 5 PM, you'll get reminders at 4 PM and 4:45 PM*

---

## Common Use Cases

### Morning Routine Tasks

```bash
# Daily tasks without specific times
todo add "Review inbox" --recurrence daily --priority medium
todo add "Check calendar" --recurrence daily --priority high
todo add "Plan the day" --recurrence daily --priority high
```

### Weekly Meetings

```bash
# Monday standup at 9 AM
todo add "Monday standup" --due 2026-01-06 --due-time 09:00 \
  --recurrence weekly --remind-before 15

# Friday retrospective at 4 PM
todo add "Weekly retrospective" --due 2026-01-03 --due-time 16:00 \
  --recurrence weekly --remind-before 30
```

### Monthly Tasks

```bash
# End-of-month reporting
todo add "Submit monthly report" --due 2026-01-31 --due-time 17:00 \
  --recurrence monthly --remind-before 1440 --priority high

# Monthly review
todo add "Personal review" --recurrence monthly
```

### Project Deadlines

```bash
# Important deadline with escalating reminders
todo add "Project Alpha deliverable" --due 2026-02-15 --due-time 23:59 \
  --remind-before 10080 \  # 1 week before
  --remind-before 2880 \   # 2 days before
  --remind-before 1440 \   # 1 day before
  --remind-before 60 \     # 1 hour before
  --remind-before 15       # 15 minutes before
```

---

## Viewing and Filtering Tasks

### By Due Date

**See overdue tasks**:
```bash
todo list --overdue
```
*Shows tasks past their due date that aren't complete*

**See tasks due today**:
```bash
todo list --due-today
```

**See tasks due this week**:
```bash
todo list --due-this-week
```

**Sort all tasks by due date**:
```bash
todo list --sort-by-due
```
*Overdue tasks appear first, then sorted by due date ascending*

### By Status and Properties

**High-priority tasks due this week**:
```bash
todo list --priority high --due-this-week --sort-by-due
```

**Incomplete recurring work tasks**:
```bash
todo list --status incomplete --recurring-only --category work
```

---

## Updating Existing Tasks

### Adding Due Dates

```bash
# Add due date to existing task
todo update 8 --due 2026-01-15

# Add due date and time
todo update 8 --due 2026-01-15 --due-time 14:00
```

### Adding Reminders

```bash
# Add reminders to existing task
todo update 8 --remind-before 60 --remind-before 15
```

### Making Tasks Recurring

```bash
# Convert existing task to recurring
todo update 8 --recurrence weekly
```

### Removing Features

```bash
# Remove due date
todo update 8 --no-due

# Remove recurrence
todo update 8 --no-recurrence

# Remove all reminders
todo update 8 --no-reminders
```

---

## Understanding Task Display

When you list tasks, the display shows:

```
ID │ Title                │ Status │ Priority │ Category │ Due Date       │ Recurs │ Reminders
───┼─────────────────────┼────────┼──────────┼──────────┼────────────────┼────────┼──────────
 1 │ [OVERDUE] Pay bills  │ ☐      │ high     │ home     │ 2025-12-31 23:59 │ -      │ -
 2 │ Team meeting         │ ☐      │ medium   │ work     │ 2026-01-03 14:00 │ Weekly │ 15m before
 3 │ Daily standup        │ ☐      │ low      │ work     │ 2026-01-02 09:00 │ Daily  │ -
```

**Columns explained**:
- **Status**: ☐ (incomplete) or ☑ (complete)
- **[OVERDUE]**: Task is past due date/time and not complete
- **Due Date**: Shows date and time if set
- **Recurs**: Shows recurrence pattern (Daily, Weekly, Monthly, or "3d" for custom)
- **Reminders**: Shows first/earliest reminder (e.g., "15m before", "1h before")

---

## Tips and Best Practices

### Reminder Intervals

Common reminder intervals in minutes:
- **15 minutes** = `--remind-before 15`
- **1 hour** = `--remind-before 60`
- **1 day** = `--remind-before 1440`
- **1 week** = `--remind-before 10080`

### When to Use Recurrence

Use recurring tasks for:
- ✅ Regular meetings and events
- ✅ Daily routines and habits
- ✅ Weekly/monthly administrative tasks
- ✅ Periodic reviews and check-ins

Don't use recurring tasks for:
- ❌ One-time projects with milestones
- ❌ Tasks with variable schedules
- ❌ Tasks that might be cancelled frequently

### Managing Overdue Tasks

If you have overdue tasks:
1. Review with `todo list --overdue --sort-by-due`
2. Complete what you can: `todo complete <ID>`
3. Reschedule the rest: `todo update <ID> --due 2026-01-XX`
4. Delete if no longer relevant: `todo delete <ID>`

### Recurring Task Best Practices

- Set realistic due times (not midnight for daily tasks)
- Use reminders for important recurring tasks
- Complete recurring tasks promptly to keep schedule accurate
- If you skip a recurring task, the next instance still creates from completion date

---

## Troubleshooting

### Reminders Not Showing

**Problem**: Not receiving desktop notifications

**Solutions**:
1. Check system notification settings (allow notifications from Terminal/Command Prompt)
2. Ensure the todo app is running (reminders only work while app has background thread)
3. Verify due date and time are in the future
4. Check that reminders are set: `todo list` should show "Xm before" or "Xh before"

### Recurring Tasks Not Creating

**Problem**: Completing recurring task doesn't create next instance

**Solutions**:
1. Verify task has recurrence: `todo list --recurring-only`
2. Check that task was marked complete: `todo list --status complete`
3. Look for next instance with same title: `todo list`

### Task Shows as Overdue Immediately

**Problem**: Task is marked overdue right after creation

**Causes**:
1. Due date is in the past (check date format YYYY-MM-DD)
2. Due time is in the past for today's date
3. System clock is incorrect

**Solution**: Update due date to future: `todo update <ID> --due 2026-XX-XX`

---

## Next Steps

- Explore combining filters: `todo list --help`
- Set up your daily routine with recurring tasks
- Configure important project deadlines with multiple reminders
- Review tasks weekly with `todo list --due-this-week`

For more details on command options:
```bash
todo add --help
todo update --help
todo list --help
```

---

## Summary

You've learned how to:
- ✅ Set due dates and times for tasks
- ✅ Configure desktop notifications (reminders)
- ✅ Create recurring tasks (daily, weekly, monthly, custom)
- ✅ Filter and sort tasks by due date
- ✅ Update and manage advanced task features

Start with simple due dates, then add reminders, and finally explore recurring tasks for your routine activities!
