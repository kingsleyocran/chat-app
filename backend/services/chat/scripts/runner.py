#!/usr/bin/env python
"""Custom Scripts for the chat service

Attributes:
    cli (function)
        This command utility function is
        used to run custom console scripts
        for chat service

Examples:
    Here is an example on how to run the script

    $ python scripts/runner.py run
        >>> # Runs the application server

    $ python scripts/ruuner.py migrate
        >>> # Performs migration of database models


"""
import os
import subprocess
from typing import Any

import click

os.environ.setdefault("TESTING", "False")


@click.command()
@click.option("--port", default=8083, type=int, help="Port to run application on")
@click.option("--host", default="0.0.0.0", type=str, help="host to run application")
@click.argument("command", default="run")
def cli(port: Any, host: Any, command: Any) -> None:
    """Command line operation for chat service

    This function is used to run custom commands
    using poetry

    Examples:
        >> poetry run chat run
        >> # runs the chat service application

        >> poetry run chat migrate
        >> # migrates the chat service models

    Args:
        port (int): Port to run application on
        host (str): host name to run the application on
        command (run): name of the command to use
    """

    command_action = {
        "run": (
            "gunicorn --env DJANGO_SETTINGS_MODULE=core.settings core.wsgi -b"
            f" {host}:{port}"
        ),
        "migrate": (
            "python manage.py migrate --pythonpath . && python manage.py search_index"
            " --create"
        ),
    }

    action_to_run = command_action.get(command)
    if action_to_run is None:
        click.echo(f"{command} is not a command, execution failed")
    else:
        click.echo("Running Chat Websocket Service")
        result = subprocess.run(
            [action_to_run],
            shell=True,
            capture_output=True,
        )

        click.echo(result.stdout)
        click.echo(result.stderr)


# comment after testing locally
# if __name__ == "__main__":
# cli()
