"""Base generator for creating new MCP servers."""

from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


@dataclass
class ServerConfig:
    """Configuration for a new MCP server."""

    project_name: str
    description: str
    python_version: str
    package_name: str

    @classmethod
    def from_inputs(cls, project_name: str, description: str, python_version: str) -> "ServerConfig":
        """Create config from user inputs."""
        package_name = project_name.replace("-", "_").lower()
        return cls(project_name=project_name, description=description, python_version=python_version, package_name=package_name)


def create_new_server(project_name: str, description: str, python_version: str) -> None:
    """Create a new MCP server project."""
    config = ServerConfig.from_inputs(project_name, description, python_version)

    # Get template directory
    template_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))

    # Create project directory using absolute path
    project_dir = Path.cwd() / project_name
    if project_dir.exists():
        raise ValueError(f"Directory {project_name} already exists")

    # Create directory structure
    dirs_to_create = [
        project_dir,
        project_dir / config.package_name,
        project_dir / config.package_name / "tools",
        project_dir / config.package_name / "services",
        project_dir / config.package_name / "interfaces",
        project_dir / config.package_name / "resources",
    ]

    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Generate files from templates
    template_files = {
        # Root project files
        "root/pyproject.toml.j2": project_dir / "pyproject.toml",
        "root/README.md.j2": project_dir / "README.md",
        "root/demo_tools.py.j2": project_dir / "demo_tools.py",

        # Core server files
        "core/server_stdio.py.j2": project_dir / config.package_name / "server_stdio.py",
        "core/server_sse.py.j2": project_dir / config.package_name / "server_sse.py",
        "core/__init__.py.j2": project_dir / config.package_name / "__init__.py",

        # Services
        "services/tool_service.py.j2": project_dir / config.package_name / "services" / "tool_service.py",
        "services/resource_service.py.j2": project_dir / config.package_name / "services" / "resource_service.py",
        "services/__init__.py.j2": project_dir / config.package_name / "services" / "__init__.py",

        # Interfaces
        "interfaces/tool.py.j2": project_dir / config.package_name / "interfaces" / "tool.py",
        "interfaces/resource.py.j2": project_dir / config.package_name / "interfaces" / "resource.py",
        "interfaces/__init__.py.j2": project_dir / config.package_name / "interfaces" / "__init__.py",

        # Tools
        "tools/__init__.py.j2": project_dir / config.package_name / "tools" / "__init__.py",
        "tools/add_numbers.py.j2": project_dir / config.package_name / "tools" / "add_numbers.py",
        "tools/date_difference.py.j2": project_dir / config.package_name / "tools" / "date_difference.py",
        "tools/reverse_string.py.j2": project_dir / config.package_name / "tools" / "reverse_string.py",
        "tools/current_time.py.j2": project_dir / config.package_name / "tools" / "current_time.py",
        "tools/random_number.py.j2": project_dir / config.package_name / "tools" / "random_number.py",

        # Resources
        "resources/__init__.py.j2": project_dir / config.package_name / "resources" / "__init__.py",
        "resources/hello_world.py.j2": project_dir / config.package_name / "resources" / "hello_world.py",
        "resources/user_profile.py.j2": project_dir / config.package_name / "resources" / "user_profile.py",
    }

    template_context = {
        "config": config,
    }

    for template_name, output_path in template_files.items():
        template = env.get_template(template_name)
        content = template.render(**template_context)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
