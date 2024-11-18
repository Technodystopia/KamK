"""
This module is used to inject data from CSV files into a DuckDB database.
"""
import os
import duckdb

class DataInjector:
    """
    A class used to represent a Data Injector.

    ...

    Attributes
    ----------
    db_path : str
        a formatted string to print out the database path
    csv_dir : str
        a formatted string to print out the csv directory path
    con : duckdb.DuckDBPyConnection
        a DuckDB connection object

    Methods
    -------
    connect_to_db():
        Connects to the DuckDB database.
    create_tables():
        Creates the necessary tables in the database.
    process_csv_files():
        Processes the CSV files and injects the data into the database.
    quack():
        Starts the data processing.
    """
    def __init__(self, database_path, csv_directory):
        """
        Constructs all the necessary attributes for the DataInjector object.

        Parameters
        ----------
            database_path : str
                database path
            csv_directory : str
                csv directory path
        """
        self.db_path = database_path
        self.csv_dir = csv_directory
        self.con = None

    def connect_to_db(self):
        """Connects to the DuckDB database."""
        print("Connecting to database...")
        try:
            self.con = duckdb.connect(self.db_path)
            print("Connected to database.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def create_tables(self):
        """Creates the necessary tables in the database."""
        print("Creating tables...")
        try:
            self.con.execute(
                "CREATE TABLE IF NOT EXISTS original "
                "(node_id INT, timestamp TIMESTAMP, x INT, y INT)"
            )
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")

    def process_csv_files(self):
        """Processes the CSV files and injects the data into the database."""
        print("Processing CSV files...")
        csv_files = [f for f in os.listdir(self.csv_dir) if f.endswith('.csv')]
        for csv_file in csv_files:
            print(f"Processing file: {csv_file}")
            try:
                csv_path = os.path.join(self.csv_dir, csv_file)
                query = (
                    "INSERT INTO original "
                    "SELECT DISTINCT node_id, timestamp, x, y "
                    "FROM read_csv_auto('{}') "
                )
                self.con.execute(query.format(csv_path))
                print(f"Data inserted into 'original' from file: {csv_file}")
            except Exception as e:
                print(f"Error processing file {csv_file}: {e}")

    def quack(self):
        """
        Start the data processing.
        """
        print("Starting the process...")
        self.connect_to_db()
        if self.con is not None:
            self.create_tables()
            self.process_csv_files()
        print("Process completed.")

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    csv_dir = os.path.join(current_dir, '..', 'data', 'projekti1')
    db_path = os.path.join(current_dir, '..', 'data', 'etl.duckdb')

    processor = DataInjector(db_path, csv_dir)
    processor.quack()
