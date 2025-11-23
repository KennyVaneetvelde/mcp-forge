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
@click.option("--python-version", "-p", default=">=3.12", help="Python version requirement")
@click.option("--with-prompts/--no-prompts", default=True, help="Include prompt examples")
@click.option("--with-sampling/--no-sampling", default=True, help="Enable sampling support for AI-to-AI collaboration")
@click.option("--with-elicitation/--no-elicitation", default=True, help="Include elicitation examples for requesting user input (MCP 2025-06-18)")
@click.option("--with-roots/--no-roots", default=True, help="Enable roots support for filesystem boundaries")
@click.option("--with-completion/--no-completion", default=True, help="Enable completion support for argument autocomplete")
@click.option("--with-auth/--no-auth", default=False, help="Enable OAuth 2.1 authentication for HTTP/SSE transports (MCP spec)")
def new(project_name: str, description: str, python_version: str, with_prompts: bool, with_sampling: bool, with_elicitation: bool, with_roots: bool, with_completion: bool, with_auth: bool):
    """Create a new MCP server project with modern features.

    Examples:
        mcp-forge new my-server
        mcp-forge new my-server --with-prompts
        mcp-forge new my-server --no-sampling
        mcp-forge new my-server --with-elicitation
    """
    try:
        create_new_server(
            project_name=project_name,
            description=description or f"{project_name} MCP server",
            python_version=python_version,
            with_prompts=with_prompts,
            with_sampling=with_sampling,
            with_elicitation=with_elicitation,
            with_roots=with_roots,
            with_completion=with_completion,
            with_auth=with_auth,
        )

        # Build success message with details
        details = []
        details.append(f"📦 Project: {project_name}")
        details.append("🚀 Transports: stdio, http, sse (all included)")
        if with_prompts:
            details.append("💬 Prompts: Enabled")
        if with_sampling:
            details.append("🤖 Sampling: Enabled")
        if with_elicitation:
            details.append("🙋 Elicitation: Enabled")
        if with_roots:
            details.append("📁 Roots: Enabled")
        if with_completion:
            details.append("✨ Completion: Enabled")
        if with_auth:
            details.append("🔐 Auth: OAuth 2.1 Enabled")

        success_msg = "\n".join(details)
        console.print(
            Panel(
                Text(f"✨ Successfully created new MCP server!\n\n{success_msg}", style="green"), title="[bold green]Success[/bold green]"
            )
        )

        # Print next steps
        package_name = project_name.replace("-", "_")
        console.print("\n[bold cyan]Next steps:[/bold cyan]")
        console.print(f"  1. cd {project_name}")
        console.print("  2. uv sync  # Install dependencies")
        console.print("  3. Choose a transport to run:")
        console.print(f"     - Stdio: uv run -m {package_name}.server --transport stdio")
        console.print(f"     - HTTP:  uv run -m {package_name}.server --transport http")
        console.print(f"     - SSE:   uv run -m {package_name}.server --transport sse")
        console.print("\n[bold cyan]Testing your server:[/bold cyan]")
        console.print("  • Interactive demo client:")
        console.print("    python demo.py  # Interactive menu to explore all features")
        console.print("  • Automated testing:")
        console.print("    python demo.py --mode test  # Run comprehensive test suite")
        console.print("  • MCP Inspector (official GUI testing tool by Anthropic):")
        console.print(f"    npx @modelcontextprotocol/inspector -- uv run -m {package_name}.server --transport stdio")
        console.print("    Opens a browser-based GUI for testing tools, resources, and prompts")

    except Exception as e:
        console.print(Panel(Text(str(e), style="red"), title="[bold red]Error[/bold red]"))


if __name__ == "__main__":
    main()
