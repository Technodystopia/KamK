"""
This module is used to connect to a DuckDB database, fetch all tables, 
write the content of each table to a text file.
"""

import pandas as pd
import duckdb

DUCKDB_FILE = 'data/testdata.duckdb'
RESULT_FILE = 'data/results/testresult.txt'

conn = duckdb.connect(DUCKDB_FILE)
tables = conn.execute("PRAGMA show_tables").fetchdf()['name'].tolist()

with open(RESULT_FILE, 'a', encoding='utf-8') as f:
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        f.write(f"Table: {table}\n")
        f.write(df.to_string())
        f.write("\n\n")

print("All tables and their content have been written to testresult.txt.")
