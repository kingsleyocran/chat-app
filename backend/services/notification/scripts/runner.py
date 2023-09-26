#!/usr/bin/env python
"""Custom Scripts for the notification service

Attributes:
    cli (function)
        This command utility function is
        used to run custom console scripts
        for notification service

Examples:
    Here is an example on how to run the script

    $ python scripts/runner.py run
        >>> # Runs the application server



"""

import subprocess

import click


@click.command()
@click.argument("command", default="run")
def cli(command) -> None:
    """Command line operation for notification service

    This function is used to run custom commands
    using poetry

    Examples:
        >> poetry run notification run
        >> # runs the notification service application


    Args:
        command (run): name of the command to use
    """
    command_action = {
        "run": (
            "celery -A main worker --loglevel=INFO & celery -A main flower"
            " --loglevel=INFO --address=0.0.0.0 --port=8083"
        ),
    }

    action_to_run = command_action.get(command)
    if action_to_run is None:
        click.echo(f"{command} is not a command, execution failed")
    else:
        click.echo("Running Notification Service")
        result = subprocess.run(
            [action_to_run],
            shell=True,
            capture_output=True,
        )

        click.echo(result.stdout)
        click.echo(result.stderr)


# comment after testing locally
# if __name__ == "__main__":
#    cli()
