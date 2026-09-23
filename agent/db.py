from contextlib import contextmanager
from typing import Iterator

from agent.config import settings


def _connection_string() -> str:
    base = (
        f"DRIVER={{{settings.sql_driver}}};SERVER={settings.sql_server};"
        f"DATABASE={settings.sql_database};Encrypt=yes;TrustServerCertificate=yes;"
    )
    if settings.sql_trusted_connection:
        return base + "Trusted_Connection=yes;"
    if not settings.sql_username or not settings.sql_password:
        raise RuntimeError("SQL credentials are required when trusted connection is disabled")
    return base + f"UID={settings.sql_username};PWD={settings.sql_password};"


@contextmanager
def connect() -> Iterator:
    try:
        import pyodbc
    except ImportError as exc:
        raise RuntimeError("pyodbc is required for live SQL execution") from exc
    connection = pyodbc.connect(_connection_string(), timeout=5)
    try:
        yield connection
    finally:
        connection.close()


def query_rows(sql: str, params: tuple = ()) -> list[dict]:
    statement = sql.lstrip().lower()
    if not statement.startswith(("select", "with")):
        raise ValueError("SupplyChain360 agent database access is read-only")
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        columns = [item[0] for item in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
