import os
import pandas as pd
import duckdb
from tqdm import tqdm
from multiprocessing import Pool

def process_csv_file(filename):
    print(f"Processing {filename}...")
    df = pd.read_csv(os.path.join('data/projekti1', filename))
    start_area = df[(df['x'] >= 600) & (df['x'] <= 900) & (df['y'] >= 2350) & (df['y'] <= 2965)]
    end_area = df[(df['x'] >= 0) & (df['x'] <= 200) & (df['y'] >= 0) & (df['y'] <= 2100)]
    df = df.sort_values('timestamp')
    filtered_df = pd.DataFrame()
    for i in tqdm(range(len(start_area) - 1), desc=f"Processing {filename}"):
        current_start_timestamp = start_area.iloc[i]['timestamp']
        next_start_timestamp = start_area.iloc[i + 1]['timestamp']
        travel_data = df[(df['timestamp'] > current_start_timestamp) & (df['timestamp'] < next_start_timestamp)]
        filtered_df = pd.concat([filtered_df, travel_data])
    temp_filename = f"{filename}_temp.csv"
    filtered_df.to_csv(temp_filename, index=False)
    print(f"Finished processing {filename}")
    return temp_filename

def process_csv_files():
    con = duckdb.connect('tokmanni.duckdb')
    con.execute("""
    CREATE TABLE IF NOT EXISTS tokmanni (
        node_id INTEGER,
        timestamp TIMESTAMP,
        x INTEGER,
        y INTEGER
    )
    """)
    with Pool(6) as p: #! Huom, tässä voi laittaa workereiden määrän
        filenames = [f for f in os.listdir('data/projekti1') if f.endswith(".csv")]
        print("Starting to process files...")
        temp_filenames = p.map(process_csv_file, filenames)
    print("Finished processing files. Starting to load data into the database...")
    for temp_filename in tqdm(temp_filenames, desc="Loading data into the database"):
        df = pd.read_csv(temp_filename)
        con.register('filtered_df_view', df[['node_id', 'timestamp', 'x', 'y']])
        con.execute("INSERT INTO tokmanni SELECT * FROM filtered_df_view")
        os.remove(temp_filename)
    print("Finished loading data into the database.")

if __name__ == "__main__":
    process_csv_files()
