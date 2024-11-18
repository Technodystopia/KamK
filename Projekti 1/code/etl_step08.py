"""
Data Migration Module

This module provides a class, DataProcessor, 
for migrating data from a source DuckDB database
to a target DuckDB database. It includes methods for 
connecting to databases, copying tables,
and adjusting timestamps for Daylight Saving Time (DST).

Example:
    To use this module, instantiate the DataProcessor 
    class with the paths to the source and target DuckDB 
    database files, then call the quack() method to start 
    the data migration process.

Attributes:
    None
"""
import os
import duckdb

class DataProcessor:
    """
    A class for migrating data between DuckDB databases.

    Attributes:
        source_db_path (str): The path to the source DuckDB database file.
        target_db_path (str): The path to the target DuckDB database file.
        source_con (duckdb.Connection): The connection to the source DuckDB database.
        target_con (duckdb.Connection): The connection to the target DuckDB database.
    """
    def __init__(self, source_db_path, target_db_path):
        """
        Initialize DataProcessor with the paths to the source and target DuckDB databases.

        Args:
            source_db_path (str): The path to the source DuckDB database file.
            target_db_path (str): The path to the target DuckDB database file.
        """
        self.source_db_path = source_db_path
        self.target_db_path = target_db_path
        self.source_con = None
        self.target_con = None

    def connect_to_db(self):
        """
        Connect to the source and target DuckDB databases.
        """
        print("Connecting to databases...")
        try:
            self.source_con = duckdb.connect(self.source_db_path)
            self.target_con = duckdb.connect(self.target_db_path)
            print("Connected to databases.")
        except Exception as e:
            print(f"Error connecting to databases: {e}")

    def copy_table(self, source_table, target_table):
        """
        Copy data from a source table to a target table.

        Args:
            source_table (str): The name of the source table.
            target_table (str): The name of the target table.
        """
        print(f"Copying data from {source_table} to {target_table}...")
        try:
            data = self.source_con.execute(f"SELECT * FROM {source_table}").fetchdf()
            self.target_con.execute(f"DROP TABLE IF EXISTS {target_table}")
            self.target_con.execute(f"""
                CREATE TABLE {target_table} 
                (node_id INT, timestamp TIMESTAMP, x INT, y INT)
            """)
            self.target_con.register('data', data)
            self.target_con.execute(f"INSERT INTO {target_table} SELECT * FROM data")
            print(f"Data copied successfully from {source_table} to {target_table}.")
        except Exception as e:
            print(f"Error copying data from {source_table} to {target_table}: {e}")

    def adjust_timestamps_for_dst(self, table_name):
        """
        Adjust timestamps for Daylight Saving Time (DST) in the specified table.

        Args:
            table_name (str): The name of the table to adjust timestamps for.
        """
        print(f"Adjusting timestamps for DST in {table_name}...")
        try:
            self.target_con.execute(f"""
                UPDATE {table_name}
                SET timestamp = timestamp + INTERVAL '2 hours'
                WHERE CAST(timestamp AS DATE) NOT BETWEEN CAST('2019-03-31' AS DATE) AND CAST('2019-10-27' AS DATE)
            """)
            self.target_con.execute(f"""
                UPDATE {table_name}
                SET timestamp = timestamp + INTERVAL '3 hours'
                WHERE CAST(timestamp AS DATE) BETWEEN CAST('2019-03-31' AS DATE) AND CAST('2019-10-27' AS DATE)
            """)
            print(f"Timestamps in {table_name} adjusted for DST.")
        except Exception as e:
            print(f"Error adjusting timestamps for DST in {table_name}: {e}")

    def quack(self):
        """
        Start the data migration process.
        """
        print("Starting the process...")
        self.connect_to_db()
        if self.source_con is not None and self.target_con is not None:
            self.copy_table('speed', 'tokmanni')
            self.copy_table('speed', 'tokmanni2')
            self.adjust_timestamps_for_dst('tokmanni2')
        print("Process completed.")

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    source_db_path = os.path.join(current_dir,'..', 'data', 'etl.duckdb')
    target_db_path = os.path.join(current_dir,'..', 'data', 'ultimate.duckdb')
    processor = DataProcessor(source_db_path, target_db_path)
    processor.quack()
