from itertools import chain
from typing import Any

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings

import db.mysql as mysql
import db.dbtypes as dbtype


mcp = MCPServer("Demo")


@mcp.tool()
def get_tables() -> list[str]:
    """Get a list of tables available in the database."""
    return mysql.get_tables()


@mcp.tool()
def get_columns(table: str) -> list[dbtype.ColumnDetail]:
    """Get a list of columns for a specified table.
    Equivalent to the result of a DESCRIBE or SHOW COLUMNS statement."""
    return mysql.get_table_definition(table)


@mcp.tool()
def get_query_result(query: str) -> list[dict[str, Any]]:
    """Get the results of an SQL query.
    Binary fields are returned as 'bytestring:' followed by a hexidecimal string.
    Hard limited to 100 rows."""
    return mysql.get_query_result(query)


good_hosts = [
    "127.0.0.1",
    "gdata-mcp-testbed.vercel.app"
]
security = TransportSecuritySettings(
    allowed_hosts=list(chain.from_iterable(map(lambda s: [s, s + ":*"], good_hosts))),
    allowed_origins=list(map(lambda s: "https://" + s, good_hosts)),
)
app = mcp.streamable_http_app(transport_security=security)


def main():
    mcp.run(transport="streamable-http", port=8000)


if __name__ == "__main__":
    main()

