"""
This module provides functionality to analyze and store data related to 'kassa'.
"""
import os
import numpy as np
import pandas as pd
import duckdb

def connect_to_db(filepath):
    """
    Connects to a DuckDB database and creates a table if it doesn't exist.

    Args:
        filepath (str): The path to the DuckDB database file.

    Returns:
        connection: A connection to the DuckDB database.
    """
    print("Connecting to the database...")
    connection = duckdb.connect(filepath)
    print("Connected to the database.")
    print("Creating table if it doesn't exist...")
    connection.execute("CREATE TABLE IF NOT EXISTS kassajono (kassa VARCHAR, node_id INTEGER, visit_start INTEGER, total_distance FLOAT, avg_time_between_visits FLOAT, total_time_of_visit FLOAT, speed FLOAT, visit_counter INTEGER)")
    print("Table created.")
    return connection

def kassa(connection, coordinates_list):
    """
    Precomputes and stores data related to 'kassa' in the database.

    Args:
        connection: A connection to the DuckDB database.
        coordinates_list (list): A list of coordinates.

    Returns:
        None
    """
    print("Crunshing and munching data")
    precomputed_data = pd.DataFrame(columns=['kassa', 'node_id', 'visit_start', 'total_distance', 'avg_time_between_visits', 'total_time_of_visit', 'speed', 'visit_counter'])

    kassa_number = 1
    for coords in coordinates_list:
        print(f"Processing coordinates for kassa-analyysi{kassa_number}...")
        x1, y1, x2, y2 = coords
        x_offset, y_offset = -781, -27
        pixel_multiplier = 9.206349
        x1_mapped = str(int(np.round(((x1 - 30) * pixel_multiplier) + x_offset, 0)))
        y1_mapped = str(int(np.round((y1 * pixel_multiplier) + y_offset, 0)))
        x2_mapped = str(int(np.round(((x2 - 30) * pixel_multiplier) + x_offset, 0)))
        y2_mapped = str(int(np.round((y2 * pixel_multiplier) + y_offset, 0)))

        df = connection.execute(f"SELECT node_id, timestamp, x, y FROM tokmanni WHERE x BETWEEN {x1_mapped} AND {x2_mapped} AND y BETWEEN {y1_mapped} AND {y2_mapped}").fetchdf()

        visit_counter = 0

        for node_id in df['node_id'].unique():
            print(f"Processing node_id {node_id}...")
            node_df = df[df['node_id'] == node_id]
            node_df = node_df.sort_values(by='timestamp')

            time_diffs = node_df['timestamp'].diff().dt.total_seconds()
            visit_counter += (time_diffs > 300).sum()

            node_df['distance'] = np.sqrt((node_df['x'].diff())**2 + (node_df['y'].diff())**2) / 100
            node_df['time_diff'] = node_df['timestamp'].diff().dt.total_seconds()
            node_df['speed'] = node_df['distance'] / node_df['time_diff']
            node_df['visit_start'] = (node_df['time_diff'] > 300).cumsum()
            node_df['visit_end'] = node_df['visit_start'].shift(-1).fillna(0).astype(int)
            node_metrics = node_df.groupby('visit_start').agg({
                'distance': 'sum',
                'time_diff': ['mean', 'sum'],
                'speed': 'mean'
            }).reset_index()
            node_metrics.columns = ['visit_start', 'total_distance', 'avg_time_between_visits', 
                                    'total_time_of_visit', 'speed']
            node_metrics['node_id'] = node_id
            node_metrics['kassa'] = f'kassa{kassa_number}'
            node_metrics['visit_counter'] = visit_counter
            precomputed_data = pd.concat([precomputed_data, node_metrics])
        kassa_number += 1

    print("Inserting FIREBALLS!!! into the database...This will take some time - get some tea meanwhile")
    for _, row in precomputed_data.iterrows():
        connection.execute("INSERT INTO kassajono (kassa, node_id, visit_start, total_distance, avg_time_between_visits, total_time_of_visit, speed, visit_counter) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [row['kassa'], row['node_id'], row['visit_start'], row['total_distance'], row['avg_time_between_visits'], row['total_time_of_visit'], row['speed'], row['visit_counter']])

    print("Counterspell inserted into the database.")

def main():
    print("Connecting to the stats database...")
    filepath = os.path.join(os.path.dirname(__file__), '../data/stats.duckdb')
    connection = connect_to_db(filepath)
    print("Connected to the stats database.")

    filepath = os.path.join(os.path.dirname(__file__), '../data/ultimate.duckdb')
    connection = connect_to_db(filepath)

    coordinates_list = [
        (67, 32, 156, 56),
        (67, 56, 156, 83),
        (67, 83, 156, 108),
        (67, 108, 156, 133),
        (67, 133, 156, 158),
        (67, 158, 156, 183),
        (67, 183, 156, 213),
        (67, 213, 156, 244)
    ]

    kassa(connection, coordinates_list)

if __name__ == "__main__":
    main()
