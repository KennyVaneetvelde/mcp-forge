# MCP-Forge

MCP-Forge is a scaffolding tool designed to quickly bootstrap new MCP (Model Context Protocol) server projects. It generates a well-structured project with boilerplate code, example tools, resources, and testing utilities, allowing you to focus on building your server's capabilities.

> ⚠️ **Early Project**: This is an early version of MCP-Forge. The API, generated structure, and features might change as the MCP ecosystem evolves. Feedback and contributions are welcome!

## Support Development

If you find this project useful, please consider supporting its development by making a donation:

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](http://paypal.com/paypalme/KennyVaneetvelde)

Your support helps maintain and improve the project!

## Features

- Generates a complete Python project structure for an MCP server.
- Includes separate server entry points for SSE and stdio transports.
- Provides example `HelloWorld` tool and `HelloWorld`/`UserProfile` resources.
- Sets up Pydantic models for clear input/output schemas.
- Includes a basic test client (`test_client.py`) demonstrating server interaction.
- Uses `uv` for dependency management and task running.

## Installation

It's recommended to run `mcp-forge` using `uvx` (from `uv`), which handles temporary environments:

```bash
# Ensure uv is installed
uvx mcp-forge --help
```

Alternatively, you can install it globally or in a dedicated environment using `pip`:

```bash
pip install mcp-forge
mcp-forge --help
```

## Usage

### Creating a New MCP Server

The primary command is `new`, which scaffolds a new server project.

```bash
# Example using uvx (recommended)
uvx mcp-forge new my-awesome-server

# Example if installed globally/in environment
# mcp-forge new my-awesome-server
```

This command will:
1. Create a new directory named `my-awesome-server`.
2. Generate a complete project structure inside this directory (see below).
3. Set up a basic server with example tools and resources ready to run.

#### Options for `new` command:

- `--description` or `-d`: Provide a custom description for your project (used in `pyproject.toml` and `README.md`).
  ```bash
  uvx mcp-forge new my-project -d "My amazing MCP server"
  ```
- `--python-version` or `-p`: Specify the minimum required Python version (default: `>=3.10`).
  ```bash
  uvx mcp-forge new my-project -p ">=3.11"
  ```

### Generated Project Structure

MCP-Forge creates a project with the following structure:

```
my-awesome-server/
├── my_awesome_server/           # Python package for your server code
│   ├── __init__.py              # Package initialization
│   ├── server_stdio.py          # Entry point for running the server with stdio transport
│   ├── server_sse.py            # Entry point for running the server with SSE transport (HTTP)
│   ├── interfaces/              # Base classes/interfaces for tools and resources
│   │   ├── __init__.py
│   │   ├── resource.py
│   │   └── tool.py
│   ├── resources/               # Implementation of resources
│   │   ├── __init__.py
│   │   ├── hello_world.py       # Example static resource
│   │   └── user_profile.py      # Example dynamic resource with URI parameters
│   ├── services/                # Services for managing tools and resources
│   │   ├── __init__.py
│   │   ├── resource_service.py  # Handles resource registration and routing
│   │   └── tool_service.py      # Handles tool registration and execution
│   └── tools/                   # Implementation of tools
│       ├── __init__.py
│       └── hello_world.py       # Example tool with input/output schemas
├── pyproject.toml               # Project metadata and dependencies (using Hatch)
├── test_client.py               # Example client script to test server functionality
└── README.md                    # README template for the generated project
```

## Next Steps After Generation

1.  **Navigate** into the newly created project directory:
    ```bash
    cd my-awesome-server
    ```
2.  **Set up** the Python environment and install dependencies:
    ```bash
    uv venv
    uv pip install -e .
    ```
3.  **Run** the server using either SSE or stdio:
    ```bash
    # Run SSE server (default: http://0.0.0.0:6969)
    uv run python -m my_awesome_server.server_sse

    # OR Run stdio server
    # uv run python -m my_awesome_server.server_stdio
    ```
4.  In a **separate terminal**, run the test client:
    ```bash
    # Make sure you are in the project directory (my-awesome-server)
    uv run test_client.py
    ```

## About MCP

The Model Context Protocol (MCP) is a specification for enabling communication between language models (or other clients) and external tools/services (servers). It defines how servers can expose capabilities like tools and resources in a standardized way.

Learn more at the official [MCP Documentation](https://modelcontextprotocol.io/).

## Contributing

Contributions to MCP-Forge are welcome! This is an early project, so there's plenty of room for improvements and new features.

1. Fork the repository (`mcp-forge`)
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file (if generated) or the source repository for details.
