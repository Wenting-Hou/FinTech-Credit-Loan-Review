# DuckDB connection and query execution helper
import duckdb

def get_connection(db_path=":memory:"):
    return duckdb.connect(db_path)
