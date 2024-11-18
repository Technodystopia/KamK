"""
This module provides functions to analyze data from a specific 
table in a DuckDB database.
It creates several tables in a second database to store various 
statistical measures for each unique node in the original table.
"""

import duckdb
import pandas as pd
from magic import DataAnalyzer

def create_tables(conn):
    """
    Create tables in the database to store various statistical measures.
    
    Args:
        conn (duckdb.DuckDBPyConnection): 
        The database connection object.
    """
    table_names = ['count', 'median', 'kurtosis', 'skew', 'iqr', 'min',
                   'max', 'mean', 'std_dev', 'variance', 'quantile']
    for table_name in table_names:
        conn.execute(f"CREATE TABLE {table_name} (node_id INTEGER, x FLOAT, y FLOAT)")

def update_table(conn, table_name, node_id, x, y):
    """
    Insert statistical measures into the specified table.
    
    Args:
        conn (duckdb.DuckDBPyConnection): The database connection object.
        table_name (str): The name of the table to update.
        node_id (int): The node ID.
        x (float): The x-value of the statistical measure.
        y (float): The y-value of the statistical measure.
    """
    x = 'NULL' if pd.isna(x) else x
    y = 'NULL' if pd.isna(y) else y
    conn.execute(f"INSERT INTO {table_name} VALUES ({node_id}, {x}, {y})")
    print(f"{table_name.capitalize()} table updated for node {node_id}.")

def analyze_data(conn2, analyzer, table_name, unique_node_ids):
    """
    Analyze data from a specific table and store the results in another database.
    
    Args:
        conn1 (duckdb.DuckDBPyConnection): 
        The connection to the database containing the original data.
        conn2 (duckdb.DuckDBPyConnection): 
        The connection to the database where the results will be stored.
        analyzer (DataAnalyzer): The data analyzer object.
        table_name (str): The name of the table to analyze.
        unique_node_ids (list): A list of unique node IDs.
    """
    function_to_table = {
        'count': 'count',
        'median': 'median',
        'kurtosis': 'kurtosis',
        'skew': 'skew',
        'iqr': 'iqr',
        'min_value': 'min',
        'max_value': 'max',
        'sample_mean': 'mean',
        'sample_std_dev': 'std_dev',
        'variance': 'variance',
        'quantile' : 'quantile'
    }

    for node_id in unique_node_ids:
        df = analyzer.get_table_data(table_name, node_id)
        if len(df) < 2:
            print(
                f"Node {node_id} has less than 2 lines of data."
                  "Skipping statistical calculations."
            )
            continue

        for function, table in function_to_table.items():
            values = getattr(analyzer, function)(table_name, node_id)
            x, y = values.loc['x'], values.loc['y']
            update_table(conn2, table, node_id, x, y)

def main():
    """
    Connect to the databases, create tables, analyze data, and store the results.
    """
    conn1 = duckdb.connect('data/ultimate.duckdb')
    conn2 = duckdb.connect('data/stats.duckdb')

    analyzer = DataAnalyzer(conn1)
    table_name = 'tokmanni'

    create_tables(conn2)

    result = conn1.execute("SELECT DISTINCT node_id FROM tokmanni")
    df = result.fetchdf()
    unique_node_ids = df['node_id'].tolist()

    analyze_data(conn2, analyzer, table_name, unique_node_ids)

    conn2.commit()
    conn2.close()

if __name__ == "__main__":
    main()
