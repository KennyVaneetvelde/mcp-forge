<div align="center">

<img src="docs/images/banner.png" alt="MCP Forge Banner" width="100%" />

# 🔨 MCP Forge

### *The Ultimate Scaffolding Tool for Model Context Protocol Servers*

[![PyPI version](https://img.shields.io/pypi/v/mcp-forge?style=for-the-badge&logo=pypi&logoColor=white&color=2563eb)](https://pypi.org/project/mcp-forge/)
[![Python Version](https://img.shields.io/pypi/pyversions/mcp-forge?style=for-the-badge&logo=python&logoColor=white&color=2563eb)](https://pypi.org/project/mcp-forge/)
[![Downloads](https://img.shields.io/pepy/dt/mcp-forge?style=for-the-badge&logo=python&logoColor=white&color=2563eb)](https://pepy.tech/project/mcp-forge)
[![License](https://img.shields.io/github/license/KennyVaneetvelde/mcp-forge?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=2563eb)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289da?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/J3W9b5AZJR)

**Generate production-ready MCP servers in seconds**
<br>
_Fast • Modern • Feature-Complete_

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Examples](#-examples) • [Community](#-community)

---

</div>

## 🎯 What is MCP Forge?

**MCP Forge** is a powerful scaffolding CLI that generates fully-featured Model Context Protocol (MCP) servers with best practices built-in. Stop writing boilerplate and start building amazing AI integrations!

```bash
# Install
pip install mcp-forge

# Create a server
mcp-forge new my-awesome-server

# That's it! 🎉
```

Your server is ready with **tools**, **resources**, **prompts**, **authentication**, **elicitation**, **sampling**, and more!

## ✨ Features

<div align="center">
<table>
<tr>
<td width="50%" valign="top">

### 🚀 Core Features
- **Multiple Transports**
  <br>Support for `stdio`, `HTTP`, and `SSE` (Server-Sent Events) out of the box.
- **FastMCP 2.0**
  <br>Built on the official, high-performance Python MCP framework.
- **Clean Architecture**
  <br>Service layer, interfaces, and dependency injection for scalable code.
- **Type Safety**
  <br>Full Pydantic validation and type hinting throughout the codebase.

</td>
<td width="50%" valign="top">

### 🔥 Advanced Capabilities
- **OAuth 2.1 Authentication**
  <br>Secure your server with full OAuth 2.1 support (optional).
- **Smart Features**
  <br>Includes **Elicitation** (interactive inputs), **Sampling** (AI collaboration), and **Roots**.
- **Developer Experience**
  <br>Comes with a **Demo Client**, **MCP Inspector** support, and comprehensive docs.
- **Production Ready**
  <br>RFC 5424 logging, error handling, and best practices built-in.

</td>
</tr>
</table>
</div>

## 🚀 Quick Start

### Installation

```bash
# Using pip
pip install mcp-forge

# Using uv (recommended for generated projects)
uv tool install mcp-forge
```

### Create Your First Server

```bash
# Interactive mode (recommended)
mcp-forge new my-server

# With options
mcp-forge new my-server \
  --description "My awesome MCP server" \
  --with-prompts \
  --with-sampling \
  --with-elicitation
```

### Run It!

```bash
cd my-server

# Install dependencies
uv sync

# Test with interactive demo client
python demo.py

# Run automated tests
python demo.py --mode test

# Start server for Claude Desktop
python -m my_server.server --transport stdio

# Start HTTP server
python -m my_server.server --transport http --port 8000
```

### Use with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["--directory", "/path/to/my-server", "run", "my_server.server"]
    }
  }
}
```

Restart Claude Desktop and your tools are ready! 🎉

## 📖 What Gets Generated?

```
my-server/
├── my_server/
│   ├── server.py                      # Main entry point (all transports)
│   ├── server_stdio.py                # stdio-only server
│   ├── server_http.py                 # HTTP server with auth
│   ├── server_sse.py                  # SSE server with SSL/TLS
│   ├── interfaces/                    # Abstract base classes
│   │   ├── tool.py
│   │   ├── resource.py
│   │   └── prompt.py
│   ├── services/                      # Business logic layer
│   │   ├── tool_service.py
│   │   ├── resource_service.py
│   │   ├── prompt_service.py
│   │   ├── auth_service.py           # OAuth 2.1 (optional)
│   │   ├── root_service.py           # Roots (optional)
│   │   └── completion_service.py     # Completions (optional)
│   ├── tools/                         # Tool implementations
│   │   ├── add_numbers.py            # Basic arithmetic
│   │   ├── weather_tool.py           # Structured outputs
│   │   ├── reasoning_tool.py         # Sampling (optional)
│   │   ├── greeting_elicitation.py   # Elicitation (optional)
│   │   └── ...
│   ├── resources/                     # Resource implementations
│   │   ├── hello_world.py
│   │   └── user_profile.py
│   └── prompts/                       # Prompt implementations
│       ├── code_review.py
│       └── ...
├── demo.py                            # Interactive demo client
├── completions.py                     # Completion handlers (optional)
├── roots_config.py                    # Roots config (optional)
├── auth_config.py                     # Auth config (optional)
├── pyproject.toml                     # uv project config
└── README.md                          # Project documentation
```

## 💡 Examples

### Adding a Simple Tool

```python
# my_server/tools/calculator.py
from pydantic import BaseModel, Field
from my_server.interfaces.tool import Tool, ToolResponse, ToolContent

class CalculatorInput(BaseModel):
    expression: str = Field(..., description="Math expression to evaluate")

class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluates mathematical expressions"
    input_model = CalculatorInput

    async def execute(self, input_data: CalculatorInput) -> ToolResponse:
        try:
            result = eval(input_data.expression)
            return ToolResponse(
                content=[ToolContent.text(f"Result: {result}")]
            )
        except Exception as e:
            return ToolResponse(
                content=[ToolContent.text(f"Error: {e}")],
                is_error=True
            )
```

Register in `tools/__init__.py` and `server.py` - that's it!

### Tool with AI Collaboration

```python
from fastmcp import Context

class ResearchTool(Tool):
    name = "research"
    description = "AI-powered research assistant"
    input_model = ResearchInput

    async def execute(self, input_data: ResearchInput, ctx: Context) -> ToolResponse:
        # Call another AI for help
        response = await ctx.sample(
            messages=[{"role": "user", "content": input_data.query}],
            system_prompt="You are a research expert.",
            temperature=0.7
        )

        # Report progress
        await ctx.report_progress(1.0, "Research complete")

        return ToolResponse(content=[ToolContent.text(response.content)])
```

### Interactive User Input (Elicitation)

```python
class TaskTool(Tool):
    name = "create_task"
    description = "Creates a task with user confirmation"
    input_model = TaskInput

    async def execute(self, input_data: TaskInput, ctx: Context) -> ToolResponse:
        # Ask user for confirmation
        result = await ctx.elicit(
            "Create this task?",
            response_type=None  # Approval only
        )

        if result.action == "accept":
            # Create the task
            return ToolResponse(content=[ToolContent.text("Task created!")])
        else:
            return ToolResponse(content=[ToolContent.text("Cancelled")])
```

### Structured Output

```python
class WeatherData(BaseModel):
    temperature: float
    humidity: int
    condition: str

class WeatherTool(Tool):
    name = "get_weather"
    input_model = WeatherInput
    output_model = WeatherData  # Enables structured output!

    async def execute(self, input_data: WeatherInput) -> ToolResponse:
        weather = WeatherData(
            temperature=72.5,
            humidity=65,
            condition="Sunny"
        )
        return ToolResponse.from_model(weather)
```

## 🎓 Documentation

- 📘 **[Getting Started Guide](docs/GETTING_STARTED.md)** - Complete walkthrough for new users
- 📙 **[Quick Reference](docs/QUICK_REFERENCE.md)** - One-page cheat sheet for common tasks

### External Resources

- 🌐 [MCP Specification](https://spec.modelcontextprotocol.io/) - Official MCP protocol docs
- 🚀 [FastMCP Documentation](https://gofastmcp.com) - FastMCP framework docs
- 🔍 [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - Official GUI testing tool
- 🐍 [Pydantic](https://docs.pydantic.dev/) - Data validation library

## 🎨 Project Templates

MCP Forge supports different template configurations:

| Feature | Description | Flag |
|---------|-------------|------|
| **Prompts** | Reusable LLM templates | `--with-prompts` / `--no-prompts` |
| **Sampling** | AI-to-AI collaboration | `--with-sampling` / `--no-sampling` |
| **Elicitation** | Interactive user input | `--with-elicitation` / `--no-elicitation` |
| **Roots** | Filesystem boundaries | `--with-roots` / `--no-roots` |
| **Completion** | Argument autocomplete | `--with-completion` / `--no-completion` |
| **Authentication** | OAuth 2.1 system | `--with-auth` / `--no-auth` |

### Example Configurations

```bash
# Minimal server (just tools and resources)
mcp-forge new minimal-server --no-prompts --no-sampling --no-elicitation

# Full-featured server (everything enabled)
mcp-forge new full-server \
  --with-prompts \
  --with-sampling \
  --with-elicitation \
  --with-auth

# API integration server (auth + completion)
mcp-forge new api-server --with-auth --with-completion
```

## 🧪 Testing Your Server

Generated servers include multiple testing options:

### 1. Interactive Demo Client

```bash
python demo.py
```

Features:
- Menu-driven interface
- Browse and execute all tools
- Read resources
- Generate prompts
- Automated test suite

### 2. MCP Inspector (Official GUI)

```bash
npx @modelcontextprotocol/inspector uv run -m my_server.server
```

Browser-based GUI for:
- Visual tool execution
- Schema inspection
- Resource browsing
- Config export

### 3. Manual Testing

```bash
# Start server
python -m my_server.server --transport http --port 8000

# Test with curl
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
EXPOSE 8000
CMD ["uv", "run", "python", "-m", "my_server.server", "--transport", "sse", "--port", "8000"]
```

### Systemd

```ini
[Unit]
Description=My MCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/my-server
ExecStart=/usr/local/bin/uv run python -m my_server.server --transport sse --port 8443
Restart=always

[Install]
WantedBy=multi-user.target
```

### Cloud Platforms

- **Railway**: One-click deploy from GitHub
- **Fly.io**: `fly launch` and deploy
- **DigitalOcean**: Docker container on App Platform
- **AWS/GCP/Azure**: Container services or serverless

## 🌟 Showcase

Built something cool with MCP Forge? We'd love to see it!

Share your projects:
- 💬 [Discord Community](https://discord.gg/J3W9b5AZJR)
- 🐙 [GitHub Discussions](https://github.com/KennyVaneetvelde/mcp-forge/discussions)
- 🐦 Twitter with `#MCPForge`

## 🤝 Community & Support

<div align="center">

### 💬 Join Our Community

[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/J3W9b5AZJR)

Get help, share projects, and connect with other MCP developers!

### ❤️ Support Development

If MCP Forge saved you time and effort, consider supporting its development:

[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](http://paypal.me/KennyVaneetvelde)

Your support helps maintain and improve MCP Forge for everyone! 🙏

</div>

## 🛠️ Contributing

We love contributions! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs**: Open an issue with detailed reproduction steps
- 💡 **Suggest Features**: Share your ideas in GitHub Discussions
- 📝 **Improve Docs**: Fix typos, add examples, clarify explanations
- 🔧 **Submit PRs**: Add features, fix bugs, improve templates
- ⭐ **Star the Repo**: Show your support and help others discover MCP Forge

### Development Setup

```bash
# Clone the repository
git clone https://github.com/KennyVaneetvelde/mcp-forge.git
cd mcp-forge

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint code
ruff check .

# Format code
ruff format .
```

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

Please ensure:
- ✅ Code follows project style (ruff)
- ✅ Tests pass
- ✅ Documentation is updated
- ✅ Commit messages are clear

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Anthropic](https://www.anthropic.com/)** - For creating the Model Context Protocol
- **[FastMCP](https://gofastmcp.com)** - For the excellent Python MCP framework
- **[MCP Community](https://modelcontextprotocol.io/)** - For advancing AI integration standards
- **All Contributors** - Thank you for making MCP Forge better!

## 📞 Contact

- 💬 **Discord**: [Join our server](https://discord.gg/J3W9b5AZJR)
- 🐙 **GitHub**: [Issues](https://github.com/KennyVaneetvelde/mcp-forge/issues) • [Discussions](https://github.com/KennyVaneetvelde/mcp-forge/discussions)
- 📧 **Email**: support@example.com (if applicable)
- 🐦 **Twitter**: [@MCPForge](https://twitter.com/mcpforge) (if applicable)

---

<div align="center">

**Made with ❤️ by the MCP Forge Team**

⭐ **Star us on GitHub** • 💬 **Join Discord** • ❤️ **Support on PayPal**

[⬆ Back to Top](#-mcp-forge)

</div>

## 📈 Star History

<div align="center">
<a href="https://star-history.com/#KennyVaneetvelde/mcp-forge&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=KennyVaneetvelde/mcp-forge&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=KennyVaneetvelde/mcp-forge&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=KennyVaneetvelde/mcp-forge&type=Date" />
 </picture>
</a>
</div>
