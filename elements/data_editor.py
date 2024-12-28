import streamlit as st
import sqlite3
import psycopg2
import duckdb
import os


def pimped_data_editor(data, **kwargs):
    if isinstance(data, dict) and data.get("type") == "db_table":
        # If 'data' is dict and 'type':'db_table', display editable DB table
        pass
    else:
        return st.data_editor(data, **kwargs)

    required_keys = {"db_name", "db_type", "db_location", "table_name"}
    missing_keys = required_keys - data.keys()
    if missing_keys:
        st.error(f"Missing required keys: {', '.join(missing_keys)}")
        return

    db_type = data["db_type"]
    db_name = data["db_name"]
    db_location = data["db_location"]
    table_name = data["table_name"]
    db_config = data.get("db_config", {})

    try:
        conn = None
        if db_type == "sqlite":
            db_path = os.path.join(db_location, db_name)
            if not os.path.exists(db_path):
                raise FileNotFoundError(f"SQLite database not found at {db_path}")
            conn = sqlite3.connect(db_path)
        elif db_type == "postgresql":
            conn = psycopg2.connect(
                dbname=db_name,
                host=db_location,
                port=db_config.get("port", 5432),
                user=db_config.get("user"),
                password=db_config.get("password"),
            )
        elif db_type == "duckdb":
            db_path = os.path.join(db_location, db_name)
            conn = duckdb.connect(database=db_path, read_only=False)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        cursor = conn.cursor()
        if db_type in {"sqlite", "duckdb"}:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        elif db_type == "postgresql":
            query = f"SELECT to_regclass('{table_name}')"

        cursor.execute(query)
        result = cursor.fetchone()

        if not result or not result[0]:
            raise ValueError(f"Table '{table_name}' does not exist in the database.")

        st.success(
            f"Successfully connected to table '{table_name}' in {db_type} database."
        )
        st.write("Database editing functionality coming soon.")

    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if conn:
            conn.close()
