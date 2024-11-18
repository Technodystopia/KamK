"""
This script loads activity data from CSV files into a DuckDB database.

The data includes various categories of activities, and the script creates a new table in the database
with an extra 'Main_Activity' column. The CSV files are read, and the data is copied into the new table.
After each file is processed, the 'Main_Activity' column is updated with the corresponding activity category.
"""

import duckdb

def load_activity_data():
    """
    Load activity data from CSV files into a DuckDB database.
    """
    con = duckdb.connect('data/stats.duckdb')

    csv_files = {
        "activity_kids0to14.csv": "0-14-vuotiaat",
        "activity_mil-and-nat-service.csv": "varus- ja siviilipalvelu",
        "activity_others.csv": "muut",
        "activity_outsideworklife.csv": "työvoiman ulkopuolella olevat",
        "activity_seniors.csv": "eläkeläiset",
        "activity_students.csv": "opiskelijat, koululaiset",
        "activity_totals.csv": "koko väestö",
        "activity_unemployed.csv": "työttömät",
        "activity_workers.csv": "työlliset",
        "activity_workforce.csv": "työvoima"
    }

    con.execute('DROP TABLE IF EXISTS activity_data')

    con.execute('''
        CREATE TABLE activity_data (
            Category VARCHAR,
            Age_Group VARCHAR,
            Year INTEGER,
            Value INTEGER,
            Main_Activity VARCHAR
        )
    ''')

    for file, activity in csv_files.items():
        file_path = f"data/muut/aktiviteetti/{file}"
        con.execute(f'''
            COPY activity_data (Category, Age_Group, Year, Value) FROM '{file_path}' (
                FORMAT CSV,
                HEADER TRUE
            )
        ''')

        con.execute(f'''
            UPDATE activity_data 
            SET Main_Activity = '{activity}'
            WHERE Main_Activity IS NULL
        ''')
        print(f"Stats database populated with main activity category: {activity}")

    con.commit()
    con.close()

    print("Activity data loaded.")

if __name__ == "__main__":
    load_activity_data()
