from itertools import chain

from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

mcp = MCPServer("Demo")

good_hosts = [
    "claude.ai",
    "127.0.0.1",
    "mcpplaygroundonline.com"
]


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
    allowed_hosts=list(chain.from_iterable(map(lambda s: [s, s + ":*"], good_hosts))),
    allowed_origins=list(map(lambda s: "https://" + s, good_hosts)),
)
app = mcp.streamable_http_app(transport_security=security)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000)
