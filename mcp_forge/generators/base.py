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
    with_prompts: bool = True
    with_sampling: bool = True
    with_elicitation: bool = True
    with_roots: bool = True
    with_completion: bool = True
    with_auth: bool = False

    @classmethod
    def from_inputs(
        cls,
        project_name: str,
        description: str,
        python_version: str,
        with_prompts: bool = True,
        with_sampling: bool = True,
        with_elicitation: bool = True,
        with_roots: bool = True,
        with_completion: bool = True,
        with_auth: bool = False,
    ) -> "ServerConfig":
        """Create config from user inputs."""
        package_name = project_name.replace("-", "_").lower()
        return cls(
            project_name=project_name,
            description=description,
            python_version=python_version,
            package_name=package_name,
            with_prompts=with_prompts,
            with_sampling=with_sampling,
            with_elicitation=with_elicitation,
            with_roots=with_roots,
            with_completion=with_completion,
            with_auth=with_auth,
        )


def create_new_server(
    project_name: str, 
    description: str, 
    python_version: str, 
    with_prompts: bool = True, 
    with_sampling: bool = True, 
    with_elicitation: bool = True,
    with_roots: bool = True,
    with_completion: bool = True,
    with_auth: bool = False,
) -> None:
    """Create a new MCP server project."""
    config = ServerConfig.from_inputs(
        project_name, 
        description, 
        python_version, 
        with_prompts, 
        with_sampling, 
        with_elicitation,
        with_roots,
        with_completion,
        with_auth,
    )

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

    # Add prompts directory if enabled
    if config.with_prompts:
        dirs_to_create.append(project_dir / config.package_name / "prompts")

    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Generate files from templates
    template_files = {
        # Root project files
        "root/pyproject.toml.j2": project_dir / "pyproject.toml",
        "root/README.md.j2": project_dir / "README.md",
        "root/demo.py.j2": project_dir / "demo.py",
        # Core server files
        "core/server.py.j2": project_dir / config.package_name / "server.py",
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
        "tools/weather_tool.py.j2": project_dir / config.package_name / "tools" / "weather_tool.py",
        # Resources
        "resources/__init__.py.j2": project_dir / config.package_name / "resources" / "__init__.py",
        "resources/hello_world.py.j2": project_dir / config.package_name / "resources" / "hello_world.py",
        "resources/user_profile.py.j2": project_dir / config.package_name / "resources" / "user_profile.py",
    }

    # Always add all transport files
    template_files["core/server_stdio.py.j2"] = project_dir / config.package_name / "server_stdio.py"
    template_files["core/server_http.py.j2"] = project_dir / config.package_name / "server_http.py"
    template_files["core/server_sse.py.j2"] = project_dir / config.package_name / "server_sse.py"

    # Add prompt files if enabled
    if config.with_prompts:
        template_files.update(
            {
                "interfaces/prompt.py.j2": project_dir / config.package_name / "interfaces" / "prompt.py",
                "services/prompt_service.py.j2": project_dir / config.package_name / "services" / "prompt_service.py",
                "prompts/__init__.py.j2": project_dir / config.package_name / "prompts" / "__init__.py",
                "prompts/code_review.py.j2": project_dir / config.package_name / "prompts" / "code_review.py",
                "prompts/data_analysis.py.j2": project_dir / config.package_name / "prompts" / "data_analysis.py",
                "prompts/debug_assistant.py.j2": project_dir / config.package_name / "prompts" / "debug_assistant.py",
            }
        )

    # Add sampling tool if enabled
    if config.with_sampling:
        template_files.update(
            {
                "tools/reasoning_tool.py.j2": project_dir / config.package_name / "tools" / "reasoning_tool.py",
            }
        )

    # Add elicitation tools if enabled
    if config.with_elicitation:
        template_files.update(
            {
                "tools/greeting_elicitation.py.j2": project_dir / config.package_name / "tools" / "greeting_elicitation.py",
                "tools/task_creation_elicitation.py.j2": project_dir / config.package_name / "tools" / "task_creation_elicitation.py",
                "tools/meeting_planner_elicitation.py.j2": project_dir / config.package_name / "tools" / "meeting_planner_elicitation.py",
                "tools/approval_elicitation.py.j2": project_dir / config.package_name / "tools" / "approval_elicitation.py",
            }
        )

    # Add roots support if enabled
    if config.with_roots:
        template_files.update(
            {
                "services/root_service.py.j2": project_dir / config.package_name / "services" / "root_service.py",
                "root/roots_config.py.j2": project_dir / "roots_config.py",
            }
        )

    # Add completion support if enabled
    if config.with_completion:
        template_files.update(
            {
                "services/completion_service.py.j2": project_dir / config.package_name / "services" / "completion_service.py",
                "root/completions.py.j2": project_dir / "completions.py",
            }
        )

    # Add auth support if enabled
    if config.with_auth:
        template_files.update(
            {
                "services/auth_service.py.j2": project_dir / config.package_name / "services" / "auth_service.py",
                "core/auth_middleware.py.j2": project_dir / config.package_name / "auth_middleware.py",
                "root/auth_config.py.j2": project_dir / "auth_config.py",
                "root/AUTH.md.j2": project_dir / "AUTH.md",
            }
        )

    template_context = {
        "config": config,
    }

    for template_name, output_path in template_files.items():
        template = env.get_template(template_name)
        content = template.render(**template_context)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
