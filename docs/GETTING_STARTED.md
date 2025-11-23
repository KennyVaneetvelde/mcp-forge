# Getting Started with Your MCP Server

Congratulations! You've scaffolded a new MCP server. This guide will help you understand what you have and how to start building.

## 📋 Table of Contents

- [What You Have](#what-you-have)
- [Quick Start](#quick-start)
- [Running Your Server](#running-your-server)
- [Testing Your Server](#testing-your-server)
- [Adding New Tools](#adding-new-tools)
- [Working with Elicitations](#working-with-elicitations)
- [Setting Up Authentication](#setting-up-authentication)
- [Using Sampling](#using-sampling)
- [Deployment](#deployment)
- [Next Steps](#next-steps)

---

## 🎁 What You Have

Your generated MCP server includes:

### Core Components
- **Server Entry Points**: Multiple ways to run your server (stdio, HTTP, SSE)
- **Example Tools**: 5 basic tools + specialized examples demonstrating advanced features
- **Example Resources**: Static and dynamic resources with template support
- **Service Layer**: Clean architecture separating business logic from MCP handlers
- **Demo Client**: Interactive CLI for testing all features

### Optional Features (based on your selections)
- **Prompts**: Reusable LLM templates with arguments
- **Sampling**: AI-to-AI collaboration via `ctx.sample()`
- **Elicitation**: Interactive user input collection
- **Roots**: Filesystem boundary definitions
- **Completion**: Smart argument auto-completion
- **Authentication**: OAuth 2.1 implementation

### Project Structure
```
your-project/
├── your_package/
│   ├── server.py              # Main entry point (all transports)
│   ├── server_stdio.py        # stdio-only server
│   ├── server_http.py         # HTTP server with auth
│   ├── server_sse.py          # SSE server with SSL/TLS
│   ├── interfaces/            # Abstract base classes
│   ├── services/              # Business logic layer
│   ├── tools/                 # Your tool implementations
│   ├── resources/             # Your resource implementations
│   └── prompts/               # Your prompt implementations
├── demo.py                    # Interactive test client
├── pyproject.toml            # Project configuration
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 2. Run the Demo Client

The easiest way to test your server:

```bash
# Interactive mode (browse and test all features)
uv run demo.py

# Automated test suite
uv run demo.py --test
```

The demo client will:
- Start your server automatically
- Let you browse tools, resources, and prompts
- Execute tools with form-based input
- Show results with pretty formatting

### 3. Use with Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "your-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/your-project",
        "run",
        "your-package.server"
      ]
    }
  }
}
```

Restart Claude Desktop, and your tools will be available!

---

## 🏃 Running Your Server

Your server supports three transport modes:

### stdio (Default - for Desktop Apps)

```bash
# Using the unified server
python -m your_package.server --transport stdio

# Or the dedicated stdio server
python -m your_package.server_stdio
```

**Use this for:**
- Claude Desktop
- Cursor IDE
- Any MCP client that launches servers as subprocesses

### HTTP (for Web Deployments)

```bash
python -m your_package.server --transport http --port 8000

# With host binding
python -m your_package.server --transport http --host 0.0.0.0 --port 8000
```

**Use this for:**
- Web applications
- Centralized server deployments
- When you need authentication
- Multi-client scenarios

**Features:**
- Single `/mcp` endpoint for all MCP operations
- Session management
- OAuth 2.1 authentication (if enabled)
- Well-known metadata endpoints
- CORS support

### SSE (Server-Sent Events with SSL/TLS)

```bash
python -m your_package.server --transport sse --port 8000

# With SSL/TLS (recommended for production)
python -m your_package.server_sse --port 8443 \
  --cert /path/to/cert.pem \
  --key /path/to/key.pem
```

**Use this for:**
- Production HTTP deployments
- When you need SSL/TLS encryption
- Mutual TLS (mTLS) scenarios
- High-security environments

**Features:**
- Full SSL/TLS configuration
- Custom cipher suites
- Certificate validation
- Self-signed cert support (dev mode)

---

## 🧪 Testing Your Server

### Using the Interactive Demo Client (Recommended!)

Your project includes a **comprehensive demo client** (`demo.py`) that showcases ALL MCP features:

```bash
# Interactive mode - explore via menu system
python demo.py

# Automated test suite - run all tests
python demo.py --mode test

# Use SSE transport (server must be running separately)
python demo.py --transport sse
```

#### Interactive Mode Features

The demo client provides a menu-driven interface:

1. **List & Call Tools**: Browse all tools, see their parameters, and execute them with a form-based input system
2. **List & Read Resources**: Browse resources and read their contents
3. **List & Get Prompts**: Browse prompts and generate them with arguments (if enabled)
4. **Run Automated Tests**: Execute comprehensive test suite
5. **Show Server Info**: View server capabilities and configuration

**What It Tests:**
- ✅ All basic tools (AddNumbers, ReverseString, CurrentTime, etc.)
- ✅ Structured output tool (WeatherTool with nested Pydantic models)
- ✅ Resources (static and dynamic with parameters)
- ✅ Prompts with arguments (if enabled)
- ✅ Resource links in tool responses
- ✅ Progress notifications
- ✅ Logging protocol (RFC 5424)
- ✅ Sampling capability (if enabled)
- ✅ Elicitation tools (if enabled)

**Example Test Output:**
```
════════════════════════════════════════════
   Running Comprehensive Automated Tests
════════════════════════════════════════════

🔧 TESTING TOOLS
────────────────────────────────────────────────────────────
Found 11 tools

  Testing: AddNumbers - Basic arithmetic
    ✓ Result: 42...
    ✓ AddNumbers passed
  Testing: ReverseString - String manipulation
    ✓ Result: !PCM olleH...
    ✓ ReverseString passed
  ...

🌤️  TESTING STRUCTURED OUTPUTS
────────────────────────────────────────────────────────────
  Testing: get_weather - Structured output with Pydantic
    ✓ WeatherTool with structured output passed

📦 TESTING RESOURCES
────────────────────────────────────────────────────────────
Found 2 resources

  Reading: static://hello
    ✓ static://hello read successfully
  ...

════════════════════════════════════════════
           TEST SUMMARY
════════════════════════════════════════════

✓ Tools: 11/11 passed
✓ Resources: 2/2 passed
✓ Prompts: 3/3 passed

MCP Spec Features:
  ✓ Structured tool outputs (Pydantic models)
  ✓ Resource links in tool responses
  ✓ Progress notifications
  ✓ Logging protocol (RFC 5424)
  ✓ Sampling (AI-to-AI collaboration)
  ✓ Elicitation (user input requests)
  ✓ Prompts

🎉 Comprehensive test complete!
```

### Using MCP Inspector (Official GUI Tool)

The **MCP Inspector** is Anthropic's official browser-based GUI for testing MCP servers:

```bash
# Install and run in one command (recommended)
npx @modelcontextprotocol/inspector uv run -m your_package.server --transport stdio
```

This opens `http://localhost:5173` in your browser with a full GUI where you can:

- 📋 **Browse Tools**: See all tools, their parameters, and descriptions
- ▶️ **Execute Tools**: Fill out forms and run tools interactively
- 📖 **Read Resources**: Browse and read all resources
- 💬 **Generate Prompts**: Create prompts with arguments
- 📤 **Export Config**: Get Claude Desktop/Cursor configuration automatically
- 🔍 **Inspect Schemas**: View JSON schemas for inputs/outputs
- 📊 **See Results**: View tool results with syntax highlighting

**For HTTP/SSE servers:**
```bash
# Start your server first
python -m your_package.server --transport http --port 8000

# Then run inspector without launching server
npx @modelcontextprotocol/inspector
# Enter http://localhost:8000/mcp in the UI
```

Learn more: [MCP Inspector Documentation](https://github.com/modelcontextprotocol/inspector)

### Manual Testing with curl

```bash
# Start HTTP server
python -m your_package.server --transport http --port 8000

# Initialize connection
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test", "version": "1.0"}
    },
    "id": 1
  }'

# List tools
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 2}'

# Call a tool
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "AddNumbers",
      "arguments": {"number1": 10, "number2": 32}
    },
    "id": 3
  }'
```

### What to Test

- ✅ **Basic Tools**: Try all example tools with different inputs
- ✅ **Structured Output**: Test WeatherTool to see nested JSON responses
- ✅ **Resources**: Access static and dynamic resources with parameters
- ✅ **Prompts**: Test prompts with various arguments (if enabled)
- ✅ **Elicitations**: Verify interactive input collection (if enabled)
- ✅ **Sampling**: Check AI-to-AI reasoning with ReasoningTool (if enabled)
- ✅ **Authentication**: Test token validation (if enabled)
- ✅ **Error Handling**: Try invalid inputs, missing parameters
- ✅ **Progress**: Watch progress updates in long-running tools
- ✅ **Logging**: Check log messages in tool execution

---

## 🛠️ Adding New Tools

### Step 1: Create a Tool Class

Create a new file in `your_package/tools/`:

```python
# your_package/tools/my_custom_tool.py
from pydantic import BaseModel, Field
from your_package.interfaces.tool import Tool, ToolResponse, ToolContent

class MyCustomToolInput(BaseModel):
    """Input schema for your tool"""
    text: str = Field(..., description="Text to process")
    count: int = Field(1, description="How many times", ge=1, le=10)

class MyCustomTool(Tool):
    name = "my_custom_tool"
    description = "Does something amazing with text"
    input_model = MyCustomToolInput

    async def execute(self, input_data: MyCustomToolInput) -> ToolResponse:
        """Execute your tool logic"""
        result = input_data.text * input_data.count

        return ToolResponse(
            content=[
                ToolContent.text(f"Result: {result}")
            ]
        )
```

### Step 2: Register the Tool

Add it to `your_package/tools/__init__.py`:

```python
from .my_custom_tool import MyCustomTool

__all__ = [
    # ... existing tools ...
    "MyCustomTool",
]
```

### Step 3: That's It!

Your server automatically discovers and registers all tools in `__all__`. Restart your server and the tool will be available.

### Advanced Tool Features

#### Using Context for AI Collaboration

```python
from fastmcp import Context

class ReasoningTool(Tool):
    name = "advanced_reasoning"
    description = "Uses AI to solve complex problems"
    input_model = ReasoningInput

    async def execute(self, input_data: ReasoningInput, ctx: Context) -> ToolResponse:
        # Call another AI for help
        response = await ctx.sample(
            messages=[{"role": "user", "content": input_data.problem}],
            system_prompt="You are a logical reasoner.",
            temperature=0.7,
            max_tokens=500
        )

        # Log information
        ctx.info(f"AI responded with: {response.content}")

        # Report progress
        await ctx.report_progress(0.5, "Halfway done")

        return ToolResponse(
            content=[ToolContent.text(response.content)]
        )
```

#### Structured Output

```python
class OutputModel(BaseModel):
    status: str
    data: dict
    timestamp: str

class MyTool(Tool):
    name = "structured_tool"
    input_model = MyInput
    output_model = OutputModel  # Enables structured output!

    async def execute(self, input_data: MyInput) -> ToolResponse:
        result = OutputModel(
            status="success",
            data={"key": "value"},
            timestamp="2025-01-01T00:00:00Z"
        )
        return ToolResponse.from_model(result)
```

#### Resource Links

```python
return ToolResponse(
    content=[
        ToolContent.text("Created user profile"),
        ToolContent.resource_link(
            uri="user://profile/user123",
            description="View the created profile"
        )
    ]
)
```

---

## 💬 Working with Elicitations

Elicitations let you collect information from users interactively. Here are common patterns:

### Simple Value Collection

```python
from fastmcp import Context
from fastmcp.exceptions import ElicitationCancelledException

async def execute(self, input_data: Input, ctx: Context) -> ToolResponse:
    # Ask for a single value
    result = await ctx.elicit(
        "What's your preferred language?",
        response_type=str
    )

    # Check if user cancelled
    if result.action == "cancel":
        return ToolResponse(
            content=[ToolContent.text("Operation cancelled")]
        )

    # Check if user declined
    if result.action == "decline":
        return ToolResponse(
            content=[ToolContent.text("User declined to provide input")]
        )

    # Use the data
    language = result.data
    return ToolResponse(
        content=[ToolContent.text(f"You chose: {language}")]
    )
```

### Structured Data Collection

```python
from pydantic import BaseModel
from typing import Literal

class UserPreferences(BaseModel):
    theme: Literal["light", "dark"]
    language: str
    notifications: Literal["enabled", "disabled"]

async def execute(self, input_data: Input, ctx: Context) -> ToolResponse:
    # Collect multiple fields at once
    result = await ctx.elicit(
        "Please set your preferences:",
        response_type=UserPreferences
    )

    if result.action == "accept":
        prefs = result.data
        return ToolResponse(
            content=[ToolContent.text(
                f"Theme: {prefs.theme}, Language: {prefs.language}"
            )]
        )
```

**Important:** MCP spec only supports shallow objects (no nesting, arrays, or nested objects).

### Multi-Turn Elicitation

```python
async def execute(self, input_data: Input, ctx: Context) -> ToolResponse:
    # Step 1: Get title
    title_result = await ctx.elicit("Meeting title?", response_type=str)
    if title_result.action != "accept":
        return ToolResponse(content=[ToolContent.text("Cancelled")])

    # Step 2: Get duration
    duration_result = await ctx.elicit(
        "Duration in minutes?",
        response_type=int
    )
    if duration_result.action != "accept":
        return ToolResponse(content=[ToolContent.text("Cancelled")])

    # Step 3: Get urgency
    urgent_result = await ctx.elicit(
        "Is this urgent?",
        response_type=Literal["yes", "no"]
    )
    if urgent_result.action != "accept":
        return ToolResponse(content=[ToolContent.text("Cancelled")])

    # Create meeting with all collected data
    meeting = {
        "title": title_result.data,
        "duration": duration_result.data,
        "urgent": urgent_result.data == "yes"
    }

    return ToolResponse(
        content=[ToolContent.text(f"Created: {meeting}")]
    )
```

### Approval/Confirmation

```python
async def execute(self, input_data: Input, ctx: Context) -> ToolResponse:
    # Ask for approval (no data collection)
    result = await ctx.elicit(
        "This will delete all data. Continue?",
        response_type=None
    )

    if result.action == "accept":
        # Proceed with destructive operation
        return ToolResponse(content=[ToolContent.text("Data deleted")])
    else:
        return ToolResponse(content=[ToolContent.text("Operation cancelled")])
```

### Best Practices

1. **Always check the action**: Don't assume `accept`
2. **Provide clear prompts**: Tell users exactly what you need
3. **Use appropriate types**:
   - `str` for text
   - `int`/`float` for numbers
   - `Literal["a", "b"]` for choices
   - `None` for approval only
4. **Handle cancellation gracefully**: Return a meaningful response
5. **Multi-turn pattern**: Check for cancellation after each step

---

## 🔐 Setting Up Authentication

If you enabled authentication, your server includes OAuth 2.1 support.

### Configuration

Edit `auth_config.py`:

```python
class AuthConfig:
    # OAuth 2.1 settings
    ISSUER = "https://your-auth-provider.com"
    AUTHORIZATION_ENDPOINT = f"{ISSUER}/oauth/authorize"
    TOKEN_ENDPOINT = f"{ISSUER}/oauth/token"
    USERINFO_ENDPOINT = f"{ISSUER}/userinfo"
    JWKS_URI = f"{ISSUER}/.well-known/jwks.json"

    # Supported scopes
    SUPPORTED_SCOPES = [
        "tools:list",      # List available tools
        "tools:call",      # Execute tools
        "resources:list",  # List resources
        "resources:read",  # Read resources
        "prompts:list",    # List prompts
        "prompts:get",     # Get prompts
        "roots:list",      # List roots
        "server:admin",    # Admin access
    ]

    # Paths that don't require auth
    EXEMPT_PATHS = [
        "/.well-known/oauth-authorization-server",
        "/.well-known/oauth-protected-resource",
        "/health",
    ]
```

### Integration Examples

#### Auth0

```python
# In auth_config.py
ISSUER = "https://your-tenant.auth0.com"
JWKS_URI = f"{ISSUER}/.well-known/jwks.json"

# In auth_service.py, add custom validator
async def validate_auth0_token(token: str) -> Optional[AccessToken]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AuthConfig.ISSUER}/userinfo",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            user_info = response.json()
            return AccessToken(
                access_token=token,
                token_type="Bearer",
                scope=" ".join(AuthConfig.SUPPORTED_SCOPES),
                expires_at=None
            )
    return None

# Register the validator
auth_service.register_token_validator(validate_auth0_token)
```

#### Okta

```python
# In auth_config.py
ISSUER = "https://your-domain.okta.com/oauth2/default"
AUTHORIZATION_ENDPOINT = f"{ISSUER}/v1/authorize"
TOKEN_ENDPOINT = f"{ISSUER}/v1/token"
USERINFO_ENDPOINT = f"{ISSUER}/v1/userinfo"
JWKS_URI = f"{ISSUER}/v1/keys"
```

#### Custom Validation

```python
# In your_package/services/auth_service.py
class AuthService:
    def __init__(self):
        # ... existing code ...

        # Add your custom validator
        self.register_token_validator(self._validate_custom_tokens)

    async def _validate_custom_tokens(self, token: str) -> Optional[AccessToken]:
        # Your custom logic
        if token.startswith("custom_"):
            # Validate against your system
            is_valid = await your_validation_logic(token)
            if is_valid:
                return AccessToken(
                    access_token=token,
                    token_type="Bearer",
                    scope="tools:call resources:read",
                    expires_at=None
                )
        return None
```

### Testing Authentication

#### Generate a Test Token (Dev Mode)

```bash
# Start HTTP server
python -m your_package.server --transport http --port 8000

# Get a test token
curl http://localhost:8000/dev/token
# Returns: {"access_token": "test_...", "token_type": "Bearer", ...}
```

#### Use the Token

```bash
# With curl
curl -H "Authorization: Bearer test_..." \
  http://localhost:8000/mcp/tools/list

# With demo client (add auth support)
uv run demo.py --transport sse --url http://localhost:8000/sse \
  --token "test_..."
```

#### Well-Known Endpoints

Your server exposes OAuth metadata:

```bash
# Authorization server metadata (RFC 8414)
curl http://localhost:8000/.well-known/oauth-authorization-server

# Protected resource metadata (RFC 9470)
curl http://localhost:8000/.well-known/oauth-protected-resource
```

### Production Deployment

1. **Disable dev token endpoint**: Set `DEV_MODE = False` in `auth_config.py`
2. **Use real OAuth provider**: Configure Auth0, Okta, Keycloak, etc.
3. **Enable SSL/TLS**: Use SSE transport with valid certificates
4. **Implement token refresh**: Add refresh token support
5. **Set token expiration**: Use `expires_at` in `AccessToken`
6. **Audit logging**: Log all authentication events

---

## 🤖 Using Sampling

Sampling lets your tools call other AI models for help.

### Basic Usage

```python
from fastmcp import Context

async def execute(self, input_data: Input, ctx: Context) -> ToolResponse:
    # Call an AI model
    response = await ctx.sample(
        messages=[
            {"role": "user", "content": "Explain quantum computing"}
        ],
        system_prompt="You are a physics expert.",
        temperature=0.7,
        max_tokens=500
    )

    return ToolResponse(
        content=[ToolContent.text(response.content)]
    )
```

### Multi-Step Reasoning

```python
async def execute(self, input_data: Input, ctx: Context) -> ToolResponse:
    # Step 1: Analyze the problem
    ctx.info("Step 1: Analyzing problem...")
    analysis = await ctx.sample(
        messages=[{"role": "user", "content": f"Analyze: {input_data.problem}"}],
        system_prompt="Break down the problem into components.",
        temperature=0.3
    )

    # Step 2: Generate solution
    ctx.info("Step 2: Generating solution...")
    await ctx.report_progress(0.5, "Halfway through")

    solution = await ctx.sample(
        messages=[
            {"role": "user", "content": f"Problem: {input_data.problem}"},
            {"role": "assistant", "content": analysis.content},
            {"role": "user", "content": "Now provide a solution."}
        ],
        system_prompt="Provide detailed solutions.",
        temperature=0.5
    )

    # Step 3: Validate
    ctx.info("Step 3: Validating solution...")
    await ctx.report_progress(0.9, "Almost done")

    validation = await ctx.sample(
        messages=[{"role": "user", "content": f"Validate this: {solution.content}"}],
        system_prompt="Check for errors and provide feedback.",
        temperature=0.2
    )

    await ctx.report_progress(1.0, "Complete")

    return ToolResponse(
        content=[
            ToolContent.text(f"Analysis:\n{analysis.content}"),
            ToolContent.text(f"\nSolution:\n{solution.content}"),
            ToolContent.text(f"\nValidation:\n{validation.content}")
        ]
    )
```

### Include Server Context

```python
# Give the AI access to your server's tools/resources/prompts
response = await ctx.sample(
    messages=[{"role": "user", "content": "What tools are available?"}],
    include_context="thisServer"  # Includes your server's capabilities
)
```

### Best Practices

1. **Use appropriate temperatures**:
   - 0.1-0.3: Factual, deterministic tasks
   - 0.5-0.7: Creative tasks
   - 0.8-1.0: Maximum creativity

2. **Set reasonable token limits**: Don't use max_tokens=10000 for simple tasks

3. **Report progress**: Use `ctx.report_progress()` for long operations

4. **Log steps**: Use `ctx.info()`, `ctx.warning()`, `ctx.error()` for debugging

5. **Handle errors**: Wrap in try/except and return meaningful errors

---

## 🗺️ Configuring Roots (Filesystem Boundaries)

If you enabled roots, your server includes a `roots_config.py` file that defines filesystem boundaries.

### What Are Roots?

Roots tell MCP clients which directories and URIs your server has access to. This helps clients:
- Understand your server's scope
- Display available directories to users
- Validate file paths
- Show workspace boundaries

### Configuration

Edit `roots_config.py`:

```python
from pathlib import Path
from your_package.services.root_service import RootDefinition

def get_default_roots():
    """Get default root definitions for this server."""
    return [
        RootDefinition(
            uri=f"file://{Path.cwd().as_posix()}",
            name="Project Workspace"
        ),
        RootDefinition(
            uri=f"file:///home/user/documents",
            name="Documents"
        ),
        RootDefinition(
            uri="file:///var/data",
            name="Data Directory"
        ),
        # Non-file URIs also supported
        RootDefinition(
            uri="https://api.example.com",
            name="Example API"
        ),
    ]
```

### Best Practices

1. **Be specific**: Only expose directories your server actually needs
2. **Use absolute paths**: Avoid relative paths that might change
3. **Document purpose**: Use clear names explaining what each root is for
4. **Security**: Never expose sensitive directories (/etc, /home, etc.)

### Accessing in Tools

```python
class FileReadTool(Tool):
    async def execute(self, input_data: Input) -> ToolResponse:
        # Clients know your server can access these roots
        # Validate paths against roots for security
        pass
```

---

## ⌨️ Setting Up Argument Completion

If you enabled completion, your server includes smart autocomplete for prompt and resource arguments.

### What Is Completion?

Argument completion provides autocomplete suggestions as users type arguments in MCP clients. This improves UX by:
- Suggesting valid values
- Preventing typos
- Providing context-aware options
- Limiting to 100 suggestions per spec

### How It Works

1. **User starts typing** an argument value
2. **Client requests completions** from server with partial value
3. **Server returns suggestions** filtered by the partial value
4. **Client displays** suggestions to user

### Configuration

Edit `completions.py` to add completion handlers:

```python
async def complete_language_argument(value: str, context: Dict[str, Any]) -> List[str]:
    """Provide completion suggestions for 'language' argument.

    Args:
        value: Current partial value being typed
        context: Other resolved argument values

    Returns:
        List of completion suggestions (max 100)
    """
    languages = ["python", "javascript", "typescript", "java", "go", "rust"]

    # Filter based on current value
    if not value:
        return languages

    value_lower = value.lower()
    return [lang for lang in languages if lang.startswith(value_lower)]
```

### Context-Aware Completion

Completions can depend on other arguments:

```python
async def complete_framework_argument(value: str, context: Dict[str, Any]) -> List[str]:
    """Framework suggestions based on selected language."""
    language = context.get("language", "").lower()

    frameworks_by_language = {
        "python": ["django", "flask", "fastapi", "pytorch"],
        "javascript": ["react", "vue", "angular", "express"],
        "typescript": ["react", "vue", "angular", "nextjs"],
    }

    frameworks = frameworks_by_language.get(language, [])

    if not value:
        return frameworks

    return [fw for fw in frameworks if fw.startswith(value.lower())]
```

### Registering Completions

In your `server.py`, completions are registered like this:

```python
from your_package.services.completion_service import CompletionService
from completions import complete_language_argument, complete_framework_argument

completion_service = CompletionService()

# For prompts
completion_service.register_completion(
    "ref/prompt",           # Reference type
    "code_review",          # Prompt name
    "language",             # Argument name
    complete_language_argument  # Handler function
)

completion_service.register_completion(
    "ref/prompt",
    "code_review",
    "framework",
    complete_framework_argument
)

# For resources (if you have dynamic resources with arguments)
completion_service.register_completion(
    "ref/resource",
    "user_profile",
    "user_id",
    complete_user_id_argument
)

completion_service.register_mcp_handlers(mcp)
```

### Best Practices

1. **Limit results**: Return max 100 suggestions (MCP spec requirement)
2. **Fast responses**: Keep completion handlers quick (< 100ms)
3. **Relevant filtering**: Filter based on partial value
4. **Clear values**: Return human-readable options
5. **Consistent casing**: Use lowercase for matching

---

## ⚙️ Environment Variables & Configuration

### Available Environment Variables

```bash
# Logging
MCP_LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR

# HTTP/SSE Server
MCP_HOST=0.0.0.0               # Host to bind to
MCP_PORT=8000                  # Port to listen on

# Authentication (if enabled)
MCP_AUTH_ISSUER=https://auth.example.com
MCP_AUTH_JWKS_URI=https://auth.example.com/.well-known/jwks.json
MCP_AUTH_AUDIENCE=your-server
MCP_DEV_MODE=true              # Enable dev token endpoint

# Custom settings
DATABASE_URL=postgresql://...
API_KEY=your-api-key
```

### Using Environment Variables

Create a `.env` file:

```bash
# .env
MCP_LOG_LEVEL=DEBUG
MCP_PORT=8080
API_KEY=sk-1234567890
DATABASE_URL=postgresql://localhost/mydb
```

Load in your code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# In server.py or config files
PORT = int(os.getenv("MCP_PORT", 8000))
HOST = os.getenv("MCP_HOST", "127.0.0.1")
LOG_LEVEL = os.getenv("MCP_LOG_LEVEL", "INFO")

# In tools
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")
```

### Configuration Files

For complex configuration, create a `config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"

    # Database
    database_url: str

    # External APIs
    api_key: str
    api_timeout: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

Use in your code:

```python
from config import settings

# In server.py
mcp.run(transport="http", host=settings.host, port=settings.port)

# In tools
async def fetch_data():
    async with httpx.AsyncClient(timeout=settings.api_timeout) as client:
        response = await client.get(
            "https://api.example.com/data",
            headers={"Authorization": f"Bearer {settings.api_key}"}
        )
```

---

## 🚢 Deployment

### Local Development

```bash
# stdio (for Claude Desktop)
python -m your_package.server --transport stdio

# HTTP (for web testing)
python -m your_package.server --transport http --port 8000
```

### Production HTTP/SSE

#### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv sync

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "your_package.server", "--transport", "sse", "--port", "8000"]
```

```bash
docker build -t your-mcp-server .
docker run -p 8000:8000 your-mcp-server
```

#### Using systemd

```ini
# /etc/systemd/system/mcp-server.service
[Unit]
Description=MCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/your-server
ExecStart=/usr/local/bin/uv run python -m your_package.server --transport sse --port 8443
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

#### With SSL/TLS

```bash
# Generate self-signed cert (dev only)
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout key.pem -out cert.pem -days 365

# Run with SSL
python -m your_package.server_sse \
  --port 8443 \
  --cert cert.pem \
  --key key.pem
```

For production, use certificates from Let's Encrypt or your CA.

### Environment Variables

```bash
# .env file
MCP_SERVER_PORT=8000
MCP_SERVER_HOST=0.0.0.0
MCP_AUTH_ENABLED=true
MCP_AUTH_ISSUER=https://auth.example.com
MCP_LOG_LEVEL=INFO
```

```python
# In your server code
import os
from dotenv import load_dotenv

load_dotenv()

port = int(os.getenv("MCP_SERVER_PORT", 8000))
```

### Monitoring

```python
# Add health check endpoint
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}
```

```bash
# Check health
curl http://localhost:8000/health
```

---

## 🎯 Next Steps

### 1. Customize Example Tools
- Modify the example tools to fit your use case
- Remove tools you don't need
- Add domain-specific tools

### 2. Add Real Resources
- Connect to databases
- Expose file systems
- Integrate with APIs

### 3. Create Useful Prompts
- Design prompts for your specific domain
- Add argument validation
- Test with different inputs

### 4. Implement Authentication
- Choose an OAuth provider
- Configure scopes appropriately
- Test with real tokens
- Secure your endpoints

### 5. Deploy to Production
- Choose a deployment method (Docker, systemd, cloud)
- Set up SSL/TLS
- Configure monitoring
- Set up logging
- Implement error tracking

### 6. Integrate with Clients
- Add to Claude Desktop
- Build web UI
- Create CLI tools
- Develop SDKs for your language

### 7. Optimize Performance
- Add caching where appropriate
- Optimize database queries
- Use connection pooling
- Profile slow operations

### 8. Write Tests
- Unit tests for tools
- Integration tests for services
- End-to-end tests with demo client
- Load testing for production

---

## 📚 Additional Resources

- **MCP Specification**: https://spec.modelcontextprotocol.io/
- **FastMCP Documentation**: https://github.com/jlowin/fastmcp
- **OAuth 2.1 Spec**: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1
- **Pydantic Documentation**: https://docs.pydantic.dev/

---

## 🆘 Getting Help

- Check the generated `README.md` for project-specific details
- Review example tools for implementation patterns
- Test with `demo.py` to see features in action
- Read `AUTH.md` for authentication details (if enabled)

**Happy building! 🚀**
