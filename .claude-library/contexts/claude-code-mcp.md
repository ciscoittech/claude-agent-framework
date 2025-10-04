# Claude Code MCP (Model Context Protocol) Context

**Source**: https://docs.claude.com/en/docs/claude-code/mcp.md
**Purpose**: Understanding Model Context Protocol for extending Claude Code
**Auto-update**: Fetch latest from docs.claude.com

---

## MCP Overview

### What is MCP?

**Model Context Protocol (MCP)** is an open standard that enables Claude Code to:
- Connect to external data sources
- Add custom tools and capabilities
- Integrate with third-party services
- Extend functionality beyond built-in tools

### Key Concepts

**MCP Server**: A service that provides:
- **Resources**: Data sources (files, databases, APIs)
- **Tools**: Custom functions Claude can call
- **Prompts**: Reusable prompt templates

**MCP Client**: Claude Code acts as the client, connecting to MCP servers to access their capabilities.

---

## MCP Architecture

```
Claude Code (Client)
    ↓
MCP Protocol
    ↓
MCP Server (Your Code)
    ↓
External Systems (Databases, APIs, Files, etc.)
```

### Data Flow

1. Claude needs data/tool
2. Sends MCP request to server
3. Server processes request
4. Returns data/result to Claude
5. Claude uses in response

---

## Using MCP Servers

### Configuration

Add MCP servers in Claude Code settings:

```json
{
  "mcpServers": {
    "my-database": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

### Available Servers

**Official Servers**:
- `@modelcontextprotocol/server-filesystem`: Local file access
- `@modelcontextprotocol/server-github`: GitHub integration
- `@modelcontextprotocol/server-gitlab`: GitLab integration
- `@modelcontextprotocol/server-postgres`: PostgreSQL access
- `@modelcontextprotocol/server-sqlite`: SQLite access

**Community Servers**:
- Search on npm: `@modelcontextprotocol/server-*`
- Check MCP server registry

---

## Building Custom MCP Servers

### Python Example

```python
# my_mcp_server.py
from mcp.server import Server
from mcp.types import Tool, Resource

server = Server("my-server")

@server.list_resources()
async def list_resources():
    """List available resources"""
    return [
        Resource(
            uri="db://users",
            name="User Database",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    """Read a specific resource"""
    if uri == "db://users":
        users = fetch_users_from_db()
        return {"contents": [{"text": json.dumps(users)}]}

@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        Tool(
            name="search_users",
            description="Search users by name or email",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool"""
    if name == "search_users":
        results = search_users(arguments["query"])
        return {"content": [{"type": "text", "text": json.dumps(results)}]}

if __name__ == "__main__":
    server.run()
```

### TypeScript Example

```typescript
// my-mcp-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0"
}, {
  capabilities: {
    resources: {},
    tools: {}
  }
});

server.setRequestHandler("resources/list", async () => {
  return {
    resources: [
      {
        uri: "api://endpoint",
        name: "My API",
        mimeType: "application/json"
      }
    ]
  };
});

server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "fetch_data",
        description: "Fetch data from API",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string" }
          }
        }
      }
    ]
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## Framework Integration

### Use Cases for Claude Agent Framework

**1. Framework Development Database**
```python
# MCP server for framework metrics
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="query_agent_performance",
            description="Query agent performance metrics from observability DB",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_name": {"type": "string"},
                    "days": {"type": "integer"}
                }
            }
        )
    ]
```

**2. Claude Code Documentation Access**
```python
# MCP server for live docs
@server.read_resource()
async def read_resource(uri: str):
    if uri.startswith("docs://"):
        doc_path = uri.replace("docs://", "")
        content = fetch_claude_docs(doc_path)
        return {"contents": [{"text": content}]}
```

**3. Framework Code Search**
```python
# MCP server for semantic code search
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_framework_patterns":
        query = arguments["query"]
        results = semantic_search(query, "AGENT_PATTERNS.md")
        return {"content": [{"type": "text", "text": results}]}
```

### Integration with Observability

```python
# MCP server wrapping observability database
from observability.db_helper import (
    get_recent_executions,
    get_agent_performance,
    get_daily_summary
)

@server.list_tools()
async def list_tools():
    return [
        Tool(name="get_recent_executions", ...),
        Tool(name="get_agent_performance", ...),
        Tool(name="get_daily_summary", ...)
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_recent_executions":
        results = get_recent_executions(limit=arguments.get("limit", 10))
        return {"content": [{"type": "text", "text": json.dumps(results)}]}
```

---

## Best Practices

### 1. Security

**Environment Variables**:
```python
# Don't hardcode secrets
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")
```

**Input Validation**:
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # Validate inputs
    if name == "query_database":
        query = arguments.get("query", "")
        if "DROP" in query.upper() or "DELETE" in query.upper():
            raise ValueError("Destructive queries not allowed")
```

### 2. Error Handling

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        result = execute_tool(name, arguments)
        return {"content": [{"type": "text", "text": result}]}
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error: {str(e)}"
            }],
            "isError": true
        }
```

### 3. Performance

**Caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def fetch_expensive_data(id: str):
    # Cache expensive operations
    return expensive_operation(id)
```

**Async Operations**:
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # Use async for I/O
    result = await async_fetch_data(arguments["id"])
    return {"content": [{"type": "text", "text": result}]}
```

### 4. Logging

```python
import logging

logger = logging.getLogger(__name__)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.info(f"Tool called: {name} with {arguments}")
    try:
        result = execute_tool(name, arguments)
        logger.info(f"Tool {name} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}")
        raise
```

---

## Common Patterns

### Pattern 1: Database Access

```python
# MCP server for observability database
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="query_metrics",
            description="Query observability metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "query_metrics":
        with get_db() as conn:
            cursor = conn.execute(arguments["sql"])
            results = [dict(row) for row in cursor.fetchall()]
        return {"content": [{"type": "text", "text": json.dumps(results)}]}
```

### Pattern 2: External API Integration

```python
# MCP server for Claude Code docs API
@server.read_resource()
async def read_resource(uri: str):
    if uri.startswith("docs://"):
        doc_path = uri.replace("docs://", "")
        response = await fetch_docs(doc_path)
        return {"contents": [{"text": response.text}]}
```

### Pattern 3: File System Access

```python
# MCP server for framework files
@server.list_resources()
async def list_resources():
    patterns = glob.glob(".claude-library/**/*.md", recursive=True)
    return [
        Resource(
            uri=f"file://{path}",
            name=path,
            mimeType="text/markdown"
        )
        for path in patterns
    ]
```

---

## Troubleshooting

### Server Not Connecting
- Check command and args are correct
- Verify server starts without errors
- Check environment variables are set
- Review Claude Code logs

### Tools Not Appearing
- Verify `list_tools()` returns correct schema
- Check tool names are unique
- Ensure server is running
- Restart Claude Code

### Slow Performance
- Add caching for expensive operations
- Use async for I/O operations
- Limit resource scans
- Profile server performance

---

## Framework Self-Building Use Cases

### 1. Live Documentation Server

```python
# Fetch latest Claude Code docs in real-time
@server.read_resource()
async def read_resource(uri: str):
    if uri == "docs://best-practices":
        content = await fetch_url("https://www.anthropic.com/engineering/claude-code-best-practices")
        return {"contents": [{"text": content}]}
```

### 2. Framework Metrics Server

```python
# Access observability data via MCP
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "analyze_agent_performance":
        perf = get_agent_performance()
        analysis = analyze_performance(perf)
        return {"content": [{"type": "text", "text": json.dumps(analysis)}]}
```

### 3. Pattern Search Server

```python
# Semantic search across framework patterns
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "find_pattern":
        query = arguments["query"]
        patterns = search_patterns(query)
        return {"content": [{"type": "text", "text": json.dumps(patterns)}]}
```

---

## Resources

**Official Docs**:
- MCP Guide: https://docs.claude.com/en/docs/claude-code/mcp.md
- SDK Docs: https://docs.claude.com/en/docs/claude-code/sdk/sdk-mcp.md
- MCP Specification: https://modelcontextprotocol.io

**Framework Integration**:
- Observability: `.claude-library/observability/`
- Best Practices: `claude-code-best-practices.md`
- Subagents: `claude-code-subagents.md`

---

**Last Updated**: October 4, 2025
**Update Method**: `/update-docs` command or WebFetch
