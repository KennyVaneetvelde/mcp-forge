# Technology Stack

## Build System & Package Management
- **Build System**: Hatchling (modern Python packaging)
- **Package Manager**: `uv` (fast Python package installer and resolver)
- **Python Version**: Requires Python >=3.10

## Core Dependencies
- **Click**: Command-line interface framework (>=8.0.0)
- **Jinja2**: Template engine for code generation (>=3.0.0)
- **Rich**: Terminal formatting and output (>=10.0.0)

## Development Tools
- **Ruff**: Python linter and formatter
  - Target version: Python 3.10
  - Line length: 140 characters
  - Quote style: double quotes
  - Indent style: spaces

## Common Commands

### Installation & Setup
```bash
# Install using uvx (recommended)
uvx mcp-forge --help

# Or install globally
pip install mcp-forge
```

### Development
```bash
# Set up development environment
uv venv
uv pip install -e .

# Run linting and formatting
ruff check .
ruff format .
```

### Usage
```bash
# Create new MCP server project
uvx mcp-forge new my-server
uvx mcp-forge new my-server -d "Custom description" -p ">=3.11"
```

## Code Style Guidelines
- Use double quotes for strings
- Maximum line length: 140 characters
- Follow PEP 8 with Ruff configuration
- Use type hints consistently
- Prefer dataclasses for configuration objects
