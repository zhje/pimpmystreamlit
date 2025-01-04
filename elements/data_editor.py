import duckdb
import os
import pandas as pd
import psycopg2
import sqlite3
import streamlit as st


def pimped_data_editor(data, **kwargs):
    # If 'data' is dict and 'type':'db_table', display editable DB table
    if isinstance(data, dict) and data.get("type") == "db_table":
        # Validate input keys
        required_keys = {"db_name", "db_type", "db_location", "table_name"}
        missing_keys = required_keys - data.keys()
        if missing_keys:
            st.error(f"Missing required keys: {', '.join(missing_keys)}")
            return

        db_type = data["db_type"]
        db_name = data["db_name"]
        db_location = data["db_location"]
        table_name = data["table_name"]

        try:
            conn = None

            if db_type == "sqlite":
                # Connect to SQLite database
                db_path = os.path.join(db_location, db_name)
                if not os.path.exists(db_path):
                    raise FileNotFoundError(f"SQLite database not found at {db_path}")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Load table data
                query = f"SELECT * FROM {table_name}"
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                # Display data editor
                original_df = pd.DataFrame(rows, columns=columns)
                edited_df = st.data_editor(original_df, num_rows="dynamic", **kwargs)

            elif db_type == "postgresql":
                conn = psycopg2.connect(
                    dbname=db_name,
                    host=db_location,
                    port=db_config.get("port", 5432),
                    user=db_config.get("user"),
                    password=db_config.get("password"),
                )
                # Finish this part
                st.error(f"Unsupported database type (temporarily): {db_type}")

            elif db_type == "duckdb":
                db_path = os.path.join(db_location, db_name)
                conn = duckdb.connect(database=db_path, read_only=False)
                # Finish this part
                st.error(f"Unsupported database type (temporarily): {db_type}")

            else:
                raise ValueError(f"Unsupported database type: {db_type}")

            # Save button
            if st.button("Save Changes"):
                # Save changes back to the database
                if not edited_df.equals(original_df):
                    cursor.execute(f"DELETE FROM {table_name}")
                    edited_df.to_sql(table_name, conn, if_exists="append", index=False)
                    conn.commit()
                    st.rerun()

        except Exception as e:
            st.error(f"An error occurred: {e}")

        finally:
            conn.close()
    else:
        return st.data_editor(data, **kwargs)
