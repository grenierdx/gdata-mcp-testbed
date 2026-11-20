from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

mcp = MCPServer("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"


@mcp.prompt()
def summarize(text: str) -> str:
    """Summarize a piece of text in one sentence."""
    return f"Summarize the following text in one sentence:\n\n{text}"


security = TransportSecuritySettings(
    allowed_hosts=["claude.ai", "claude.ai:*", "127.0.0.1", "127.0.0.1:*"],
    allowed_origins=["https://claude.ai", "https://localhost"],
)
app = mcp.streamable_http_app(transport_security=security)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000)
