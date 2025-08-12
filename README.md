# MCP-Forge 🔨

MCP-Forge is a modern scaffolding tool for quickly bootstrapping Model Context Protocol (MCP) server projects in Python. It generates well-structured projects following the latest MCP specifications (2025-03-26) with FastMCP 2.0 integration.

> 📢 **Version 0.3.0**: Major update with improved architecture, dual transport support, and FastMCP integration.

## Support Development

If you find this project useful, please consider supporting its development:

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](http://paypal.com/paypalme/KennyVaneetvelde)

Your support helps maintain and improve the project!

## ✨ Features

- 🚀 **Dual Transports**: stdio (recommended) and HTTP transport (using SSE)
- 🛠️ **Tools**: 5 ready-to-use example tools with full type validation
- 📦 **Resources**: Static and dynamic resource examples with URI patterns
- 💬 **Prompts**: Template structure for prompt implementations
- 🏗️ **Clean Architecture**: Service-based design with clear interfaces
- 📝 **FastMCP**: Built on the FastMCP Python framework
- 🔄 **Development Mode**: Auto-reload support for faster iteration
- ⚡ **uv Integration**: Fast dependency management and project setup
- 🧪 **Demo Clients**: Comprehensive testing tools included

## Installation

Recommended: Use `uvx` for temporary environments:

```bash
# Run directly with uvx
uvx mcp-forge --help
```

Or install globally:

```bash
pip install mcp-forge
mcp-forge --help
```

## Quick Start

### Create a New MCP Server

```bash
# Basic usage
uvx mcp-forge new my-server

# With options
uvx mcp-forge new my-server \
  --description "My amazing MCP server" \
  --transport both \
  --with-prompts \
  --with-sampling
```

### Command Options

- `--description` / `-d`: Project description
- `--python-version` / `-p`: Python version requirement (default: `>=3.10`)
- `--transport` / `-t`: Transport mechanism (`stdio`, `http`, `both`) (default: `both`)
- `--with-prompts` / `--no-prompts`: Include prompt examples (default: enabled)
- `--with-sampling` / `--no-sampling`: Enable sampling support (default: enabled)

### Examples

```bash
# HTTP-only server for web deployment
uvx mcp-forge new web-server --transport http

# Minimal stdio server without extras
uvx mcp-forge new simple-server --transport stdio --no-prompts --no-sampling

# Full-featured server with everything
uvx mcp-forge new full-server --transport both --with-prompts --with-sampling
```

## Generated Project Structure

```
my-server/
├── my_server/
│   ├── __init__.py
│   ├── server.py                # Unified entry point (NEW)
│   ├── server_stdio.py          # stdio transport
│   ├── server_http.py           # HTTP transport (SSE-based)
│   ├── interfaces/
│   │   ├── tool.py
│   │   ├── resource.py
│   │   └── prompt.py            # Prompt interface (NEW)
│   ├── services/
│   │   ├── tool_service.py
│   │   ├── resource_service.py
│   │   └── prompt_service.py    # Prompt management (NEW)
│   ├── tools/
│   │   ├── add_numbers.py
│   │   ├── date_difference.py
│   │   ├── reverse_string.py
│   │   ├── current_time.py
│   │   └── random_number.py
│   ├── resources/
│   │   ├── hello_world.py
│   │   └── user_profile.py
│   └── prompts/                 # Prompt templates (NEW)
│       ├── code_review.py
│       ├── data_analysis.py
│       └── debug_assistant.py
├── pyproject.toml
└── README.md
```

## Using Your Generated Server

### 1. Setup

```bash
cd my-server
uv venv
uv pip install -e .
```

### 2. Run the Server

```bash
# Unified entry point (recommended)
python -m my_server.server --transport stdio  # For Claude Desktop, Cursor
python -m my_server.server --transport http   # For web deployments

# With options
python -m my_server.server --transport http --port 8080 --reload
```

### 3. Test Your Server

Use the included demo client to test all features:

```bash
# Test with stdio transport
python demo_client.py --transport stdio

# Test with HTTP transport (start server first)
python demo_client.py --transport http --url http://localhost:8000

# Interactive testing mode
python demo_client.py --transport http --interactive
```

### 4. Configure with Claude Desktop

Add to Claude Desktop config:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_server.server", "--transport", "stdio"]
    }
  }
}
```

## What's New in v0.3.0

### Breaking Changes
- ❌ **Standalone SSE module removed** - Unified transport system
- 📝 **Unified server entry** - New `server.py` with `--transport` flag
- 🔄 **FastMCP import changes** - Now uses `from fastmcp import FastMCP`

### New Features
- ✅ **HTTP transport** - Web-ready communication (SSE-based in FastMCP 2.x)
- 💬 **Prompts support** - Reusable message templates
- 🤖 **Sampling capability** - AI-to-AI collaboration
- 🎯 **Transport selection** - Choose stdio, HTTP, or both
- 📦 **FastMCP 2.0** - Latest framework integration

### Migration from v0.2.x

If you have existing servers:
1. Use the new unified server entry point
2. Update imports to use `fastmcp` instead of `mcp.server.fastmcp`
3. Choose transport via `--transport` flag
4. Note: HTTP transport currently uses SSE under the hood

## Testing MCP Servers

MCP-Forge includes a universal demo client (`demo_mcp_client.py`) that can test any MCP server:

### Features
- Test both stdio and HTTP transports
- Automatic discovery of tools, resources, and prompts
- Interactive and automated testing modes
- Comprehensive test suite with examples
- Beautiful terminal UI with rich formatting

### Usage

```bash
# Test any stdio server
python demo_mcp_client.py --transport stdio --module my_server

# Test any HTTP server (SSE endpoint)
python demo_mcp_client.py --transport http --url http://localhost:8000

# Interactive mode
python demo_mcp_client.py --transport http --interactive --url http://localhost:8000

# Run full test suite
python demo_mcp_client.py --transport stdio --module my_server --test-all
```

### What It Tests
- **Tools**: Executes each tool with sample arguments
- **Resources**: Reads static and dynamic resources
- **Prompts**: Generates prompts with example inputs
- **Capabilities**: Displays server capabilities and features
- **Performance**: Measures response times

## About MCP

The Model Context Protocol (MCP) is an open standard that enables seamless communication between LLMs and external tools/services. It provides a unified way to expose capabilities like tools, resources, and prompts.

Learn more:
- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com)
- [Anthropic's MCP Announcement](https://www.anthropic.com/news/model-context-protocol)

## Contributing

Contributions are welcome! This project follows modern MCP standards and best practices.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the existing code style and patterns
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/yourusername/mcp-forge
cd mcp-forge
uv venv
uv pip install -e .
```

## Roadmap

- [ ] Add more transport options (WebSocket, gRPC)
- [ ] Template customization system
- [ ] Plugin architecture for extensions
- [ ] Testing utilities and examples
- [ ] CLI tool for adding components to existing projects
- [ ] Integration with popular frameworks

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Anthropic for creating the Model Context Protocol
- FastMCP team for the excellent Python framework
- The MCP community for feedback and contributions

---

Built with ❤️ for the MCP ecosystem