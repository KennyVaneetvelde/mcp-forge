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
@click.option("--with-prompts/--no-prompts", default=True, help="Include prompt examples")
@click.option("--with-sampling/--no-sampling", default=True, help="Enable sampling support for AI-to-AI collaboration")
def new(project_name: str, description: str, python_version: str, with_prompts: bool, with_sampling: bool):
    """Create a new MCP server project with modern features.

    Examples:
        mcp-forge new my-server
        mcp-forge new my-server --with-prompts
        mcp-forge new my-server --no-sampling
    """
    try:
        create_new_server(
            project_name=project_name,
            description=description or f"{project_name} MCP server",
            python_version=python_version,
            with_prompts=with_prompts,
            with_sampling=with_sampling,
        )

        # Build success message with details
        details = []
        details.append(f"📦 Project: {project_name}")
        details.append("🚀 Transports: stdio, http, sse (all included)")
        if with_prompts:
            details.append("💬 Prompts: Enabled")
        if with_sampling:
            details.append("🤖 Sampling: Enabled")

        success_msg = "\n".join(details)
        console.print(
            Panel(
                Text(f"✨ Successfully created new MCP server!\n\n{success_msg}", style="green"), title="[bold green]Success[/bold green]"
            )
        )

        # Print next steps
        console.print("\n[bold cyan]Next steps:[/bold cyan]")
        console.print(f"  1. cd {project_name}")
        console.print("  2. uv venv && uv pip install -e .")
        console.print("  3. Choose a transport to run:")
        console.print("     - Stdio: python -m {} --transport stdio".format(project_name.replace("-", "_")))
        console.print("     - HTTP:  python -m {} --transport http".format(project_name.replace("-", "_")))
        console.print("     - SSE:   python -m {} --transport sse".format(project_name.replace("-", "_")))

    except Exception as e:
        console.print(Panel(Text(str(e), style="red"), title="[bold red]Error[/bold red]"))


if __name__ == "__main__":
    main()
