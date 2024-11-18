"""
This module connects to a DuckDB database, retrieves the row count for each table,
and writes the results to a text file.
"""

import duckdb

def main():
    """Main function to execute the script."""
    conn = duckdb.connect('data/ultimate.duckdb')

    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

    with open('data/results/dbsize.txt', 'w', encoding='utf-8') as f:
        for table in tables:
            count = conn.execute(f'SELECT COUNT(*) FROM {table[0]}').fetchone()[0]
            f.write(f'Table {table[0]}: {count} rows\n')

    print("The number of rows in each table has been written to 'dbsize.txt'.")

if __name__ == "__main__":
    main()
