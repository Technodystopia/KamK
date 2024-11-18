"""
Data Processing Module

This module contains a class, DataProcessor, for processing 
data stored in a DuckDB database.
It provides methods for connecting to the database, 
creating tables, calculating speed,
filtering data based on speed and distance criteria, 
and orchestrating the entire data processing process.

Example:
    To use this module, instantiate the DataProcessor class with 
    the path to the DuckDB database file,
    then call the quack() method to start the data processing process.

Attributes:
    None
"""

import os
import duckdb

class DataProcessor:
    """
    A class to process data in a DuckDB database.
    
    Attributes:
        db_path (str): The path to the DuckDB database file.
        con (duckdb.Connection): The connection to the DuckDB database.
    """
    def __init__(self, database_path):
        """
        Initialize DataProcessor with the path to the DuckDB database.

        Args:
            database_path (str): The path to the DuckDB database file.
        """
        self.db_path = database_path
        self.con = None

    def connect_to_db(self):
        """
        Connect to the DuckDB database.
        """
        print("Connecting to database...")
        try:
            self.con = duckdb.connect(self.db_path)
            print("Connected to database.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def create_tables(self):
        """
        Create required tables in the database.
        """
        print("Creating tables...")
        try:
            self.con.execute(
                "CREATE TABLE IF NOT EXISTS speed "
                "(node_id INT, timestamp TIMESTAMP, x INT, y INT)"
            )
            self.con.execute(
                "CREATE TABLE IF NOT EXISTS distance "
                "(node_id INT, timestamp TIMESTAMP, x INT, y INT)"
            )
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")

    def calculate_speed_and_filter_data(self, table_name):
        """
        Calculate speed and filter data based on speed criteria.

        Args:
            table_name (str): The name of the table to perform calculations on.
        """
        print(f"Calculating speed and filtering data from {table_name}...")
        try:
            query = (
                "CREATE TABLE temp_table AS "
                "SELECT *, "
                "SQRT("
                    "POWER(x - LAG(x) OVER (PARTITION BY node_id ORDER BY timestamp), 2) + "
                    "POWER(y - LAG(y) OVER (PARTITION BY node_id ORDER BY timestamp), 2)"
                ") / "
                "ABS(EXTRACT(EPOCH FROM timestamp - "
                    "LAG(timestamp) OVER (PARTITION BY node_id ORDER BY timestamp)"
                ")) / 3600 as speed "
                "FROM {}"
            )

            self.con.execute(query.format(table_name))
            print("Speed calculated.")
        except Exception as e:
            print(f"Error calculating speed: {e}")
            return
        try:
            self.con.execute(
                "INSERT INTO speed SELECT node_id, timestamp, x, y "
                f"FROM temp_table WHERE speed <= 6"
            )
            print(
                f"Data filtered and inserted into 'speed' from '{table_name}'."
            )

        except Exception as e:
            print(f"Error filtering data and inserting into 'speed' from '{table_name}': {e}")
            return
        try:
            self.con.execute("DROP TABLE temp_table")
            print("Temporary table dropped.")
        except Exception as e:
            print(f"Error dropping temporary table: {e}")

    def filter_coordinates_by_distance(self, table_name, max_distance):
        """
        Filter coordinates based on distance criteria.

        Args:
            table_name (str): The name of the table to filter coordinates from.
            max_distance (float): The maximum distance allowed.
        """
        print(f"Filtering coordinates by distance in {table_name}...")
        try:
            query = (
                "CREATE TABLE distance_temp AS "
                "SELECT *, "
                "SQRT("
                "POWER(x - LAG(x) OVER (PARTITION BY node_id ORDER BY timestamp), 2) + "
                "POWER(y - LAG(y) OVER (PARTITION BY node_id ORDER BY timestamp), 2)"
                ") as distance "
                "FROM {}"
            )

            self.con.execute(query.format(table_name))
            print("Distance calculated.")
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return

        try:
            self.con.execute(
                "INSERT INTO distance (node_id, timestamp, x, y) "
                f"SELECT node_id, timestamp, x, y FROM {table_name} "
                f"WHERE (SELECT SQRT(POWER(x - LAG(x) OVER (PARTITION BY node_id ORDER BY timestamp), 2) + "
                f"POWER(y - LAG(y) OVER (PARTITION BY node_id ORDER BY timestamp), 2)) FROM {table_name}) <= {max_distance}"
            )
            print(
                f"Data filtered and inserted into 'distance' from '{table_name}'."
            )

        except Exception as e:
            print(f"Error filtering data and inserting into 'distance' from '{table_name}': {e}")
            return

        try:
            self.con.execute("DROP TABLE distance_temp")
            print("Temporary table dropped.")
        except Exception as e:
            print(f"Error dropping temporary table: {e}")

    def quack(self):
        """
        Start the data processing process.
        """
        print("Starting the process...")
        self.connect_to_db()
        if self.con is not None:
            self.create_tables()
            print("Speed filter started")
            self.calculate_speed_and_filter_data('time')
            print("Distance filter started")
            max_distance = 20
            self.filter_coordinates_by_distance('speed', max_distance)
        print("Process completed.")


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    db_path = os.path.join(current_dir,'..', 'data', 'etl.duckdb')
    processor = DataProcessor(db_path)
    processor.quack()
