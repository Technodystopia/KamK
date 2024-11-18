"""
Module Docstring:
A module to fetch all tables from a duckdb database and 
write the content of each table to a separate file.
"""

import os
import duckdb

class DuckDBExtractor:
    """
    Class Docstring:
    A class to extract data from duckdb database tables 
    and write the content to files.
    """

    def __init__(self, db_path, result_dir):
        self.db_path = db_path
        self.result_dir = result_dir
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Establish a connection to the database.
        """
        try:
            self.conn = duckdb.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Failed to connect to the database. Error: {str(e)}")
            return False
        return True

    def write_to_file(self, filename, data, columns):
        """
        Write data to a file.
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                f.write('\t'.join(columns) + '\n')
                for line in data:
                    f.write('\t'.join(map(str, line)) + '\n')
        except Exception as e:
            print(f"Failed to write to file: {filename}. Error: {str(e)}")

    def get_all_tables(self):
        """
        Fetch all table names from the database.
        """
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Failed to fetch tables. Error: {str(e)}")
            return []

    def get_table_content(self, table_name):
        """
        Fetch the content of a specific table.
        """
        try:
            self.cursor.execute(f'SELECT * FROM {table_name}')
            data = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return data, columns
        except Exception as e:
            print(f"Failed to fetch content from table: {table_name}. Error: {str(e)}")
            return [], []

    def process(self):
        """
        Process all tables in the database.
        """
        if not self.connect():
            return

        tables = self.get_all_tables()
        print("Fetching all tables...")
        for table in tables:
            table_name = table[0]
            print(f"Processing table: {table_name}")
            content, columns = self.get_table_content(table_name)
            file_path = os.path.join(self.result_dir, f'{table_name}.txt')
            print(f"Writing to file: {file_path}")
            self.write_to_file(file_path, content, columns)

        self.conn.close()
        print("All done!")

if __name__ == "__main__":
    db_path = os.path.join('data', 'stats.duckdb')
    result_dir = os.path.join('data', 'results')
    extractor = DuckDBExtractor(db_path=db_path, result_dir=result_dir)
    extractor.process()
