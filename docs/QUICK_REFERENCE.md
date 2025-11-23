# Quick Reference Guide

One-page reference for common tasks in your MCP server.

## 🚀 Running the Server

```bash
# stdio (Claude Desktop, Cursor)
python -m your_package.server --transport stdio

# HTTP (web deployments)
python -m your_package.server --transport http --port 8000

# SSE (Server-Sent Events)
python -m your_package.server --transport sse --port 8000

# Development mode (auto-reload)
python -m your_package.server --transport http --reload
```

## 🧪 Testing

```bash
# Interactive demo client
python demo.py

# Automated tests
python demo.py --mode test

# MCP Inspector (GUI)
npx @modelcontextprotocol/inspector uv run -m your_package.server
```

## 🛠️ Adding a Simple Tool

```python
# your_package/tools/my_tool.py
from pydantic import BaseModel, Field
from your_package.interfaces.tool import Tool, ToolResponse, ToolContent

class MyToolInput(BaseModel):
    text: str = Field(..., description="Input text")

class MyTool(Tool):
    name = "my_tool"
    description = "Does something with text"
    input_model = MyToolInput

    async def execute(self, input_data: MyToolInput) -> ToolResponse:
        result = input_data.text.upper()
        return ToolResponse(
            content=[ToolContent.text(f"Result: {result}")]
        )

# Register in tools/__init__.py
from .my_tool import MyTool
__all__ = [..., "MyTool"]

# Register in server.py get_available_tools()
return [... , MyTool()]
```

## 🤖 Tool with AI Collaboration

```python
from fastmcp import Context

async def execute(self, input_data: Input, ctx: Context) -> ToolResponse:
    # Call AI for help
    response = await ctx.sample(
        messages=[{"role": "user", "content": input_data.question}],
        temperature=0.7
    )

    # Log and report progress
    ctx.info("Processing complete")
    await ctx.report_progress(1.0, "Done")

    return ToolResponse(content=[ToolContent.text(response.content)])
```

## 💬 Tool with User Input (Elicitation)

```python
async def execute(self, input_data: Input, ctx: Context) -> ToolResponse:
    # Ask user for input
    result = await ctx.elicit("What's your name?", response_type=str)

    if result.action == "accept":
        return ToolResponse(content=[ToolContent.text(f"Hello, {result.data}!")])
    else:
        return ToolResponse(content=[ToolContent.text("Cancelled")])
```

## 📦 Adding a Resource

```python
# your_package/resources/my_resource.py
from your_package.interfaces.resource import Resource, ResourceResponse, ResourceContent

class MyResource(Resource):
    uri = "myapp://data/{id}"
    name = "My Data"
    description = "Data resource"
    mime_type = "application/json"

    async def read(self, id: str) -> ResourceResponse:
        data = {"id": id, "value": "example"}
        return ResourceResponse(
            contents=[
                ResourceContent(
                    uri=self.uri.format(id=id),
                    mime_type=self.mime_type,
                    text=json.dumps(data)
                )
            ]
        )

# Register in resources/__init__.py and server.py
```

## 🎯 Tool Return Types

```python
# Simple text
return ToolResponse(content=[ToolContent.text("Hello!")])

# JSON data
return ToolResponse(content=[ToolContent.json({"key": "value"})])

# Structured output (requires output_model)
class OutputModel(BaseModel):
    status: str
    data: dict

class MyTool(Tool):
    output_model = OutputModel

    async def execute(self, input_data) -> ToolResponse:
        result = OutputModel(status="success", data={})
        return ToolResponse.from_model(result)

# Resource link
return ToolResponse(
    content=[
        ToolContent.text("Created!"),
        ToolContent.resource_link("user://123", "View user")
    ]
)

# Multiple content items
return ToolResponse(
    content=[
        ToolContent.text("Summary"),
        ToolContent.json({"details": "..."}),
        ToolContent.resource_link("myapp://result/1", "View result")
    ]
)
```

## 🔐 Authentication (if enabled)

```python
# Get test token (dev mode)
curl http://localhost:8000/dev/token

# Use token in requests
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/mcp -d '{"method": "tools/list"}'

# Custom validator in auth_service.py
async def my_validator(token: str) -> Optional[AccessToken]:
    # Validate token
    if is_valid(token):
        return AccessToken(access_token=token, ...)
    return None

auth_service.register_token_validator(my_validator)
```

## 🗺️ Roots Configuration

```python
# roots_config.py
def get_default_roots():
    return [
        RootDefinition(
            uri=f"file://{Path.cwd().as_posix()}",
            name="Workspace"
        ),
    ]
```

## ⌨️ Argument Completion

```python
# completions.py
async def complete_language(value: str, context: Dict[str, Any]) -> List[str]:
    options = ["python", "javascript", "typescript"]
    if not value:
        return options
    return [opt for opt in options if opt.startswith(value.lower())]

# Register in server.py
completion_service.register_completion(
    "ref/prompt", "code_review", "language", complete_language
)
```

## 📊 Progress & Logging

```python
async def execute(self, input_data: Input, ctx: Context) -> ToolResponse:
    # Report progress
    await ctx.report_progress(0.25, "25% complete")
    await ctx.report_progress(0.50, "Halfway done")
    await ctx.report_progress(1.0, "Complete")

    # Log messages
    ctx.debug("Debug info")
    ctx.info("Information")
    ctx.warning("Warning message")
    ctx.error("Error occurred")

    return ToolResponse(...)
```

## 🔍 Validation with Pydantic

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import datetime

class MyInput(BaseModel):
    # Required field
    name: str = Field(..., description="User name", min_length=3, max_length=50)

    # Optional with default
    age: int = Field(18, description="User age", ge=0, le=150)

    # Constrained string
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

    # Enum/choices
    status: Literal["active", "inactive", "pending"]

    # Custom validator
    @field_validator('name')
    def validate_name(cls, v):
        if v.lower() == "admin":
            raise ValueError("'admin' is reserved")
        return v

    # Dependent validator
    @field_validator('email')
    def validate_email_domain(cls, v):
        if not v.endswith(('.com', '.org')):
            raise ValueError("Must be .com or .org")
        return v
```

## 🎨 Common Patterns

### Error Handling
```python
async def execute(self, input_data: Input) -> ToolResponse:
    try:
        result = await risky_operation()
        return ToolResponse(content=[ToolContent.text(result)])
    except ValueError as e:
        return ToolResponse(
            content=[ToolContent.text(f"Invalid input: {e}")],
            is_error=True
        )
    except Exception as e:
        return ToolResponse(
            content=[ToolContent.text(f"Error: {e}")],
            is_error=True
        )
```

### External API Call
```python
import httpx

async def execute(self, input_data: Input) -> ToolResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.example.com/data",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30.0
        )
        response.raise_for_status()
        data = response.json()

    return ToolResponse(content=[ToolContent.json(data)])
```

### Database Query
```python
from sqlalchemy import select

async def execute(self, input_data: Input) -> ToolResponse:
    async with db.session() as session:
        result = await session.execute(
            select(User).where(User.id == input_data.user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return ToolResponse(
                content=[ToolContent.text("User not found")],
                is_error=True
            )

        return ToolResponse(content=[ToolContent.json({
            "id": user.id,
            "name": user.name
        })])
```

### File Operations
```python
from pathlib import Path

async def execute(self, input_data: Input) -> ToolResponse:
    file_path = Path(input_data.path)

    # Security: Validate path
    base_path = Path.cwd()
    if not file_path.resolve().is_relative_to(base_path):
        return ToolResponse(
            content=[ToolContent.text("Access denied")],
            is_error=True
        )

    # Read file
    if file_path.exists() and file_path.is_file():
        content = file_path.read_text()
        return ToolResponse(content=[ToolContent.text(content)])
    else:
        return ToolResponse(
            content=[ToolContent.text("File not found")],
            is_error=True
        )
```

## 📝 Claude Desktop Configuration

```json
{
  "mcpServers": {
    "your-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/project",
        "run",
        "your_package.server"
      ]
    }
  }
}
```

On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## 🔗 Useful Links

- **MCP Spec**: https://spec.modelcontextprotocol.io/
- **FastMCP Docs**: https://gofastmcp.com
- **MCP Inspector**: https://github.com/modelcontextprotocol/inspector
- **Pydantic**: https://docs.pydantic.dev/

## 💡 Tips

1. **Always validate inputs** with Pydantic field validators
2. **Use Context** for AI collaboration, logging, and elicitation
3. **Test with demo.py** before deploying
4. **Check MCP Inspector** for schema validation
5. **Use structured outputs** for complex return data
6. **Report progress** for long-running operations
7. **Handle errors gracefully** and return helpful messages
8. **Secure file paths** to prevent traversal attacks
9. **Use environment variables** for secrets and configuration
10. **Read the getting started guide** for detailed explanations!
