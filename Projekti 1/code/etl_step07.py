"""
Data Count Module

This module provides functions to count rows by node ID in a DuckDB database.

Example:
    To use this module, execute the main() function. It connects to the DuckDB database,
    retrieves all tables, counts rows for each table grouped by node ID, and writes
    the results to a file named 'creator.txt' in the 'data/results' directory.

Attributes:
    None
"""

import duckdb

def count_rows_by_node_id(connection, table_name):
    """
    Count rows by node ID in the specified table.

    Args:
        connection (duckdb.Connection): The connection to the DuckDB database.
        table_name (str): The name of the table to count rows from.

    Returns:
        list: A list of tuples containing node ID and row count.
    """
    query = f"SELECT node_id, COUNT(*) FROM {table_name} GROUP BY node_id"
    result = connection.execute(query).fetchall()
    return result

def main():
    """
    Main function to count rows by node ID for all tables in the database
    and write the results to a file.
    """
    connection = duckdb.connect(database='data/etl.duckdb')
    tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    with open("data/results/creator.txt", "w") as f:
        for table in tables:
            table_name = table[0]
            f.write(f"Table: {table_name}\n")
            results = count_rows_by_node_id(connection, table_name)
            for node_id, count in results:
                f.write(f"Node ID: {node_id}, Row Count: {count}\n")
            f.write("\n")

if __name__ == "__main__":
    main()
