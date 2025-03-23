# MCP-Forge

MCP-Forge is a scaffolding tool for creating new MCP (Modular Capability Platform) servers. It helps you quickly generate the boilerplate code needed to start building MCP-compatible servers.

> ⚠️ **Early Project**: This is a very early version of MCP-Forge and may have some rough edges. The API and features might change as the MCP ecosystem evolves.

## Installation

Install MCP-Forge using `uv`:

```bash
uvx @uv mcp-forge
```

Or with pip:

```bash
pip install mcp-forge
```

## Usage

### Creating a New MCP Server

To create a new MCP server project:

```bash
mcp-forge new my-awesome-server
```

This will:
1. Create a new directory with your project name
2. Generate a complete project structure with all necessary files
3. Set up a basic server with example tools and resources

#### Options

- `--description` or `-d`: Project description
- `--python-version` or `-p`: Python version requirement (default: ">=3.10")

```bash
mcp-forge new my-project --description "My amazing MCP server" --python-version ">=3.11"
```

### Generated Project Structure

MCP-Forge creates a project with the following structure:

```
my-awesome-server/
├── my_awesome_server/
│   ├── __init__.py
│   ├── server_stdio.py
│   ├── server_sse.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── tool.py
│   │   └── resource.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── tool_service.py
│   │   └── resource_service.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── hello_world.py
│   └── resources/
│       ├── __init__.py
│       ├── hello_world.py
│       └── user_profile.py
├── pyproject.toml
├── test_client_stdio.py
├── test_client_sse.py
└── README.md
```

## About MCP

The Modular Capability Platform (MCP) is a framework for building modular, extensible services that can expose tools and resources in a standardized way. MCP servers can be integrated with various clients, including AI assistants, to provide enhanced capabilities.

## Contributing

Contributions are welcome! This is an early project, so there's plenty of room for improvements and new features.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
