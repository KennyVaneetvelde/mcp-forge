# Project Structure

## Root Directory Layout
```
mcp-forge/
├── mcp_forge/              # Main Python package
├── .kiro/                  # Kiro IDE configuration
├── .venv/                  # Python virtual environment
├── dist/                   # Build artifacts
├── pyproject.toml          # Project configuration
├── README.md               # Project documentation
├── LICENSE                 # MIT license
└── uv.lock                 # Dependency lock file
```

## Main Package Structure (`mcp_forge/`)
```
mcp_forge/
├── __init__.py             # Package initialization with version
├── cli.py                  # Click-based command line interface
├── generators/             # Code generation logic
│   └── base.py            # Core generator with ServerConfig dataclass
├── templates/             # Jinja2 templates for scaffolding
│   ├── core/              # Server entry points (stdio/SSE)
│   ├── interfaces/        # Base classes for tools/resources
│   ├── resources/         # Resource implementation templates
│   ├── root/              # Project root files (pyproject.toml, README)
│   ├── services/          # Service layer templates
│   └── tools/             # Tool implementation templates
└── utils/                 # Utility functions
```

## Generated Project Structure
When MCP-Forge creates a new project, it follows this pattern:
```
my-server/
├── my_server/             # Snake_case package name
│   ├── server_stdio.py    # Stdio transport entry point
│   ├── server_sse.py      # SSE transport entry point
│   ├── interfaces/        # Base classes
│   ├── resources/         # Resource implementations
│   ├── services/          # Service layer (tool/resource management)
│   └── tools/             # Tool implementations
├── pyproject.toml         # Generated project config
└── README.md              # Generated documentation
```

## Architecture Patterns
- **Template-based generation**: Uses Jinja2 for flexible code scaffolding
- **Service layer pattern**: Separate services for tool and resource management
- **Interface segregation**: Base classes in `interfaces/` directory
- **Transport abstraction**: Separate entry points for different MCP transports
- **Configuration-driven**: Uses dataclasses for generator configuration

## File Naming Conventions
- Package names: snake_case (e.g., `my_server`)
- Module names: snake_case with descriptive names
- Template files: `.j2` extension for Jinja2 templates
- Generated projects: kebab-case converted to snake_case for packages
