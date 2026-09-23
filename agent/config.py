import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    sql_server: str = os.getenv("SC360_SQL_SERVER", "localhost")
    sql_database: str = os.getenv("SC360_SQL_DATABASE", "WideWorldImportersDW")
    sql_driver: str = os.getenv("SC360_SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    sql_trusted_connection: bool = os.getenv("SC360_SQL_TRUSTED_CONNECTION", "true").lower() == "true"
    sql_username: str | None = os.getenv("SC360_SQL_USERNAME")
    sql_password: str | None = os.getenv("SC360_SQL_PASSWORD")
    llm_provider: str = os.getenv("SC360_LLM_PROVIDER", "none")
    llm_model: str = os.getenv("SC360_LLM_MODEL", "gpt-5.6")

settings = Settings()
