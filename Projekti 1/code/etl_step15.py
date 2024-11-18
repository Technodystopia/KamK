"""
This module provides a class and functions to interact with DuckDB databases.
It includes functionality to count rows in a table and list all tables in the database.
"""

import duckdb

class DuckDBQueries:
    """
    A class used to represent a DuckDB Query.

    ...

    Attributes
    ----------
    con : duckdb.DuckDBPyConnection
        a DuckDB connection object

    Methods
    -------
    count_rows(table_name)
        Returns the number of rows in the given table.
    list_tables()
        Returns a list of all tables in the database.
    """

    def __init__(self, db_path):
        """
        Constructs all the necessary attributes for the DuckDBQueries object.

        Parameters
        ----------
            db_path : str
                path to the DuckDB database
        """

        print("Initializing DuckDBQueries...")
        self.con = duckdb.connect(database=db_path)

    def count_rows(self, table_name):
        """
        Count the number of rows in the given table.

        Parameters
        ----------
            table_name : str
                name of the table

        Returns
        -------
            row_count : int
                number of rows in the table
        """

        print(f"Counting rows in {table_name}...")
        row_count = self.con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        return row_count

    def list_tables(self):
        """
        List all tables in the database.

        Returns
        -------
            tables : list
                list of all tables in the database
        """

        print("Listing all tables...")
        result = self.con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = result.fetchall()
        return [table[0] for table in tables]

def write_results_to_file(db_path, table, row_count):
    """
    Write the results to a file.

    Parameters
    ----------
        db_path : str
            path to the DuckDB database
        table : str
            name of the table
        row_count : int
            number of rows in the table
    """

    with open('data/results/toolresults.txt', 'a') as file:
        file.write(f"{db_path} - The number of rows in the '{table}' table is {row_count}.\n")

def main():
    """
    Main function to create DuckDBQueries objects and write results to a file.
    """

    db_paths = ['data/ultimate.duckdb', 'data/stats.duckdb']
    print("Creating DuckDBQueries objects...")

    for db_path in db_paths:
        db_queries = DuckDBQueries(db_path)
        tables = db_queries.list_tables()
        for table in tables:
            row_count = db_queries.count_rows(table)
            write_results_to_file(db_path, table, row_count)

if __name__ == "__main__":
    main()
