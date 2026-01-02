"""User prompt handlers with validation."""

import click
from typing import Any, Callable, Optional


class ValidationError(Exception):
    """Exception raised when input validation fails."""

    pass


def prompt_with_validation(
    prompt_text: str,
    validator: Callable[[str], Any],
    max_attempts: int = 3,
    default: Optional[Any] = None,
) -> Optional[Any]:
    """Prompt user for input with validation and retry logic.

    Args:
        prompt_text: The prompt message to display.
        validator: Function that validates and transforms input.
        max_attempts: Maximum number of retry attempts.
        default: Default value if user presses Enter.

    Returns:
        Validated value, or None if max attempts reached.
    """
    # Add hint about cancelling with Ctrl+C
    if not prompt_text.endswith("(Press Ctrl+C to cancel)"):
        prompt_text = f"{prompt_text} (Press Ctrl+C to cancel)"

    for attempt in range(max_attempts):
        try:
            value = click.prompt(prompt_text, default=default, show_default=True)
            return validator(value)
        except ValidationError as e:
            remaining = max_attempts - attempt - 1
            click.echo(
                click.style(
                    f"Error: {e}. {remaining} attempts remaining.", fg="red"
                )
            )
        except KeyboardInterrupt:
            click.echo("\nOperation cancelled. Returning to main menu.")
            return None

    click.echo(
        click.style(
            "Max attempts reached. Returning to main menu.", fg="yellow"
        )
    )
    return None


def prompt_for_title() -> Optional[str]:
    """Prompt user for task title.

    Returns:
        Validated title or None if cancelled.
    """
    from src.cli.validation import validate_title

    return prompt_with_validation(
        prompt_text="Task title",
        validator=validate_title,
        max_attempts=3
    )


def prompt_for_description() -> Optional[str]:
    """Prompt user for task description (optional field).

    Returns:
        Validated description or empty string if skipped.
    """
    from src.cli.validation import validate_description

    click.echo("Task description (optional, press Enter to skip):")
    result = prompt_with_validation(
        prompt_text="",
        validator=validate_description,
        max_attempts=3,
        default=""
    )

    return result if result else ""


def prompt_for_priority() -> Optional[str]:
    """Prompt user for task priority with default.

    Returns:
        Validated priority or default if cancelled.
    """
    from src.cli.validation import validate_priority

    return prompt_with_validation(
        prompt_text="Task priority (high/medium/low)",
        validator=validate_priority,
        max_attempts=3,
        default="medium"
    )


def prompt_for_category() -> Optional[str]:
    """Prompt user for task category with default.

    Returns:
        Validated category or default if cancelled.
    """
    from src.cli.validation import validate_category

    return prompt_with_validation(
        prompt_text="Task category (work/home)",
        validator=validate_category,
        max_attempts=3,
        default="uncategorized"
    )
