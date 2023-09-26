#!/usr/bin/env python
"""Custom Scripts for the support service

Attributes:
    cli (function)
        This command utility function is 
        used to run custom console scripts
        for support service
        
Examples:
    Here is an example on how to run the script
    
    $ python scripts/runner.py run
        >>> # Runs the application server


"""

import subprocess

import click


@click.command()
@click.option("--port", default=8084, type=int, help="Port to run application on")
@click.option("--host", default="0.0.0.0", type=str, help="host to run application")
@click.argument("command", default="run")
def cli(port, host, command) -> None:
    """Command line operation for account service

    This function is used to run custom commands
    using poetry

    Examples:
        >> poetry run support run
        >> # runs the support service application

    Args:
        port (int): Port to run application on
        host (str): host name to run the application on
        command (run): name of the command to use
    """
    command_action = {
        "run": f"uvicorn main:app --reload --port {port} --host {host}",
    }

    action_to_run = command_action.get(command)
    if action_to_run is None:
        click.echo(f"{command} is not a command, execution failed")
    else:
        click.echo("Running Support Service")
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
