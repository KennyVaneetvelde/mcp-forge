"""Command line interface for MCP server scaffolding."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .generators.base import create_new_server

console = Console()


@click.group()
def main():
    """MCP Server Scaffolding Tool - Create and extend MCP servers with ease."""
    pass


@main.command()
@click.argument("project_name")
@click.option("--description", "-d", help="Project description")
@click.option("--python-version", "-p", default=">=3.10", help="Python version requirement")
def new(project_name: str, description: str, python_version: str):
    """Create a new MCP server project."""
    try:
        create_new_server(project_name=project_name, description=description or f"{project_name} MCP server", python_version=python_version)
        console.print(
            Panel(Text(f"✨ Successfully created new MCP server: {project_name}", style="green"), title="[bold green]Success[/bold green]")
        )
    except Exception as e:
        console.print(Panel(Text(str(e), style="red"), title="[bold red]Error[/bold red]"))


if __name__ == "__main__":
    main()
