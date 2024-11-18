"""
This module is used for loading data from a CSV file into a DuckDB database.

It uses pandas to read the CSV file and DuckDB to create a new table in the database.
The data from the CSV file is then inserted into the newly created table.

The module contains the following constants:
- CSV_FILE: The path to the CSV file.
- DUCKDB_FILE: The path to the DuckDB database file.
- TABLE_NAME: The name of the table to be created in the DuckDB database.

The module performs the following steps:
1. Reads the CSV file using pandas.
2. Connects to the DuckDB database.
3. Creates a new table in the DuckDB database using the data from the CSV file.
4. Prints a success message after the data has been inserted into the table.
"""
import pandas as pd
import duckdb

CSV_FILE1 = 'data/results/test.csv'
CSV_FILE2 = 'data/results/section.csv'
DUCKDB_FILE = 'data/testdata.duckdb'
TABLE_NAME1 = 'test_table'
TABLE_NAME2 = 'layer_table'

data = pd.read_csv(CSV_FILE1)
con = duckdb.connect(DUCKDB_FILE)
cur = con.cursor()
cur.execute(f"CREATE TABLE {TABLE_NAME1} AS SELECT * FROM read_csv_auto('{CSV_FILE1}')")
print(f"Data inserted successfully into '{TABLE_NAME1}' in '{DUCKDB_FILE}' database.")

data = pd.read_csv(CSV_FILE2)
con = duckdb.connect(DUCKDB_FILE)
cur = con.cursor()
cur.execute(f"CREATE TABLE {TABLE_NAME2} AS SELECT * FROM read_csv_auto('{CSV_FILE2}')")
print(f"Data inserted successfully into '{TABLE_NAME2}' in '{DUCKDB_FILE}' database.")