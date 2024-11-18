"""
This script loads death data from a CSV file into a DuckDB database.

The data includes various categories of deaths, and the script creates a new table in the database.
The CSV file is read, and the data is copied into the new table.
"""

import duckdb

def load_death_data():
    """
    Load death data from a CSV file into a DuckDB database.
    """
    con = duckdb.connect('data/stats.duckdb')

    con.execute('DROP TABLE IF EXISTS deaths_age_sex')

    con.execute('''
        CREATE TABLE deaths_age_sex (
            Category VARCHAR,
            Age_group VARCHAR,
            Year INTEGER,
            Value INTEGER
        )
    ''')

    con.execute('''
        COPY deaths_age_sex FROM 'data/muut/aktiviteetti/deaths_age_sex.csv' (
            FORMAT CSV,
            HEADER TRUE
        )
    ''')

    con.commit()
    con.close()

    print("Death data loaded.")

if __name__ == "__main__":
    load_death_data()
