import os

from mcp.server.mcpserver.exceptions import ToolError
from sqlalchemy import create_engine, text

from .dbtypes import ColumnDetail


# Connection variables
db_host = os.getenv("DB_HOST")
db_schema = os.getenv("DB_SCHEMA")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
# Limit results to avoid overwhelming the parser
result_hard_limit = int(os.getenv("RESULT_HARD_LIMIT", "100"))


engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_schema}", echo=True)


def get_tables():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("show tables"))
            # Execute returns rows, so limit each row to its only value
            return list(map(lambda row: row[0], result.all()))
    except Exception as e:
        raise ToolError(f"{type(e)} | {e}")


def get_table_definition(table: str):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"show full columns from {table}"))
            # Convert rows to our annotated ColumnDetail class
            return list(map(lambda row: ColumnDetail(**row._asdict()), result.all()))
    except Exception as e:
        raise ToolError(f"{type(e)} | {e}")


def get_explain_plan(query: str):
    pass # TODO: implement explain


# No query sanitization is performed! This is dangerous, so make sure the database user you
# expose to the tool is limited to select only!
def get_query_result(query: str):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            # Convert bytes to a string to avoid breaking the protocol
            rows = result.fetchmany(result_hard_limit)
            str_result_list = []
            for row in rows:
                row_as_dict = row._asdict()
                for k in row_as_dict:
                    v = row_as_dict[k]
                    if type(v) == bytes:
                        row_as_dict[k] = f"bytestring:{v.hex()}"
                str_result_list.append(row_as_dict)
            return str_result_list
    except Exception as e:
        raise ToolError(f"{type(e)} | {e}")
