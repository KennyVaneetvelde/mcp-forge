# MCP-Forge 🔨

MCP-Forge is a modern scaffolding tool for quickly bootstrapping Model Context Protocol (MCP) server projects in Python. It generates well-structured projects following the latest MCP specifications (2025-03-26) with FastMCP 2.0 integration.

> 📢 **Version 0.3.0**: Major update with improved architecture, dual transport support, and FastMCP integration.

## Support Development

If you find this project useful, please consider supporting its development:

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](http://paypal.com/paypalme/KennyVaneetvelde)

Your support helps maintain and improve the project!

## ✨ Features

- 🚀 **Multiple Transports**: stdio (recommended), HTTP, and SSE with SSL/TLS support
- 🔐 **SSL/TLS Security**: Full SSL support for SSE transport including mTLS
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
  --with-prompts \
  --with-sampling
```

### Command Options

- `--description` / `-d`: Project description
- `--python-version` / `-p`: Python version requirement (default: `>=3.10`)
- `--with-prompts` / `--no-prompts`: Include prompt examples (default: enabled)
- `--with-sampling` / `--no-sampling`: Enable sampling support (default: enabled)

### Examples

```bash
# Basic server
uvx mcp-forge new my-server

# Server with description
uvx mcp-forge new my-server --description "My awesome MCP server"

# Minimal server without extras
uvx mcp-forge new simple-server --no-prompts --no-sampling

# Full-featured server with everything
uvx mcp-forge new full-server --with-prompts --with-sampling
```

## Generated Project Structure

```
my-server/
├── my_server/
│   ├── __init__.py
│   ├── server.py                # Unified entry point
│   ├── server_stdio.py          # stdio transport
│   ├── server_http.py           # HTTP transport
│   ├── server_sse.py            # SSE transport with SSL support
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

## Transport Options

MCP-Forge supports multiple transport mechanisms, each suited for different use cases:

### stdio Transport
- **Best for**: Claude Desktop, Cursor, local development
- **Protocol**: Standard input/output communication
- **Security**: Inherits from parent process
- **Usage**: `--transport stdio`

### HTTP Transport  
- **Best for**: Web deployments, REST API integration
- **Protocol**: HTTP with request/response pattern
- **Security**: HTTPS via reverse proxy recommended
- **Usage**: `--transport http`

### SSE Transport
- **Best for**: Real-time streaming, secure communications
- **Protocol**: Server-Sent Events over HTTP/HTTPS
- **Security**: Built-in SSL/TLS and mTLS support
- **Usage**: `--transport sse`


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
python -m my_server.server --transport sse    # For SSE with optional SSL

# With options
python -m my_server.server --transport http --port 8080 --reload

# SSE with SSL/TLS
python -m my_server.server_sse --ssl-keyfile server.key --ssl-certfile server.crt

# SSE with mTLS (mutual TLS)
python -m my_server.server_sse \
  --ssl-keyfile server.key \
  --ssl-certfile server.crt \
  --ssl-ca-certs ca.crt \
  --require-client-cert
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

## SSE Transport with SSL/TLS Support

The SSE (Server-Sent Events) transport provides real-time server-to-client streaming with comprehensive SSL/TLS security features.

### SSL/TLS Features

- **Modern TLS Support**: TLS 1.2 and 1.3 with configurable cipher suites
- **Certificate Management**: Support for SSL certificates, private keys, and CA bundles
- **mTLS Support**: Client certificate verification for mutual TLS authentication
- **Environment Variables**: Configure SSL via environment for production deployments
- **Development Mode**: Instructions and tools for self-signed certificates

### Configuration Options

```bash
# Basic SSE server (no SSL)
python -m my_server.server_sse

# With SSL/TLS encryption
python -m my_server.server_sse \
  --ssl-keyfile /path/to/server.key \
  --ssl-certfile /path/to/server.crt

# With specific TLS version
python -m my_server.server_sse \
  --ssl-keyfile server.key \
  --ssl-certfile server.crt \
  --tls-version 1.3

# With client certificate verification (mTLS)
python -m my_server.server_sse \
  --ssl-keyfile server.key \
  --ssl-certfile server.crt \
  --ssl-ca-certs ca.crt \
  --require-client-cert

# Using environment variables
SSL_KEYFILE=/etc/ssl/server.key \
SSL_CERTFILE=/etc/ssl/server.crt \
python -m my_server.server_sse
```

### Generating Self-Signed Certificates

For development and testing:

```bash
# Generate a self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365 \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Generate with specific domains
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365 \
  -subj "/CN=myserver.local" \
  -addext "subjectAltName=DNS:myserver.local,DNS:localhost,IP:127.0.0.1"
```

### Production Deployment

For production environments:

1. **Use trusted certificates** from a Certificate Authority (Let's Encrypt, etc.)
2. **Enable strict TLS** with `--tls-version 1.3`
3. **Configure strong ciphers** (enabled by default)
4. **Use reverse proxy** (Nginx, Cloudflare) for SSL termination
5. **Enable mTLS** for enhanced security when appropriate

### Security Best Practices

- Always use HTTPS/TLS in production
- Keep certificates and keys secure (proper file permissions)
- Rotate certificates regularly
- Monitor certificate expiration
- Use strong cipher suites (configured by default)
- Consider using a reverse proxy for additional security layers

## What's New in v0.3.0

### Breaking Changes
- ❌ **Standalone SSE module removed** - Unified transport system
- 📝 **Unified server entry** - New `server.py` with `--transport` flag
- 🔄 **FastMCP import changes** - Now uses `from fastmcp import FastMCP`

### New Features
- ✅ **SSE transport** - Server-Sent Events with full SSL/TLS support
- 🔐 **SSL/mTLS support** - Comprehensive security features for SSE
- ✅ **HTTP transport** - Web-ready communication
- 💬 **Prompts support** - Reusable message templates
- 🤖 **Sampling capability** - AI-to-AI collaboration
- 🎯 **Transport selection** - Choose stdio, HTTP, SSE, or all
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
- Test stdio, HTTP, and SSE transports
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