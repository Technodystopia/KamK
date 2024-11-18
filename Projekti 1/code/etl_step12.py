"""
Module: StatisticalAnalysis

This module performs statistical analysis on data from the 'ultimate' 
database using DuckDB. It calculates various statistical metrics 
for each node in the 'tokmanni2' table and stores the results in 
the 'stats' database.

Functions:
    - Main: Entry point for statistical analysis.
"""
import math
import duckdb
import pandas as pd
import numpy as np
from magic import DataAnalyzer

conn1 = duckdb.connect('data/ultimate.duckdb')
conn2 = duckdb.connect('data/stats.duckdb')
analyzer = DataAnalyzer(conn1)
table_name = 'tokmanni'

conn2.execute(
    "CREATE TABLE first_last_timestamp "
    "(node_id INTEGER, first TIMESTAMP, last TIMESTAMP)"
)
conn2.execute(
    "CREATE TABLE total_distance "
    "(node_id INTEGER, distance FLOAT)"
)
conn2.execute(
    "CREATE TABLE average_speed "
    "(node_id INTEGER, speed FLOAT)"
)
conn2.execute(
    "CREATE TABLE location_noise "
    "(node_id INTEGER, timestamp TIMESTAMP, x_noise FLOAT, y_noise FLOAT)"
)
conn2.execute(
    "CREATE TABLE trend_over_time "
    "(node_id INTEGER, date DATE, x_trend FLOAT, y_trend FLOAT)"
)
conn2.execute(
    "CREATE TABLE daily_seasonality "
    "(node_id INTEGER, hour INTEGER, x_mean FLOAT, y_mean FLOAT)"
)
conn2.execute(
    "CREATE TABLE outlier_frequency "
    "(node_id INTEGER, frequency FLOAT)"
)
conn2.execute(
    "CREATE TABLE correlation "
    "(node_id INTEGER, correlation FLOAT)"
)
conn2.execute(
    "CREATE TABLE covariance "
    "(node_id INTEGER, covariance FLOAT)"
)
conn2.execute(
    "CREATE TABLE days_between_timestamps "
    "(node_id INTEGER, days INTEGER)"
)

result = conn1.execute("SELECT DISTINCT node_id FROM tokmanni2")
df = result.fetchdf()
unique_node_ids = df['node_id'].tolist()

for node_id in unique_node_ids:
    df = analyzer.get_table_data(table_name, node_id)
    if len(df) < 2:
        print(f"Node {node_id} has less than 2 lines of data. Skipping statistical calculations.")
        continue

    first_timestamp, last_timestamp = analyzer.first_last_timestamp(table_name, node_id)
    conn2.execute(
        f"INSERT INTO first_last_timestamp "
        f"VALUES ({node_id}, '{first_timestamp}', '{last_timestamp}')"
    )
    print(f"first_last_timestamp table updated for node {node_id}.")


    distance = analyzer.total_distance(table_name, node_id)
    conn2.execute(f"INSERT INTO total_distance VALUES ({node_id}, {distance})")
    print(f"total_distance table updated for node {node_id}.")

    speed = analyzer.average_speed(table_name, node_id)
    conn2.execute(f"INSERT INTO average_speed VALUES ({node_id}, {speed})")
    print(f"average_speed table updated for node {node_id}.")

    days = analyzer.days_between_timestamps(table_name, node_id)
    if days is not None:
        conn2.execute(f"INSERT INTO days_between_timestamps VALUES ({node_id}, {days})")
        print(f"days_between_timestamps table updated for node {node_id}.")

    noise_df = analyzer.location_noise(table_name, node_id)
    if not isinstance(noise_df.index, pd.DatetimeIndex):
        noise_df.index = pd.to_datetime(noise_df.index)
    daily_avg_noise_df = noise_df.resample('D').mean()
    total_rows = len(daily_avg_noise_df)
    for timestamp, row in daily_avg_noise_df.iterrows():
        x_noise_avg = row['x']
        y_noise_avg = row['y']
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f%z')
        if np.isnan(x_noise_avg) or np.isnan(y_noise_avg):
            print(f"Skipping row with nan values at timestamp {timestamp_str}")
            continue
        conn2.execute(
            f"INSERT INTO location_noise VALUES "
            f"({node_id}, '{timestamp_str}', {x_noise_avg}, {y_noise_avg})"
        )
        total_rows -= 1
        if total_rows % 100 == 0:
            print(f"Remaining rows to insert for node {node_id}: {total_rows}")
    print(f"location_noise table updated for node {node_id} with daily averages.")

    trend_df = analyzer.trend_over_time(table_name, node_id)
    total_rows = len(trend_df)
    for date, row in trend_df.iterrows():
        x_trend = row['x']
        y_trend = row['y']
        if pd.isna(x_trend) or pd.isna(y_trend):
            print(f"Skipping insert for node {node_id} on date {date} due to NaN value")
            continue
        conn2.execute(
            f"INSERT INTO trend_over_time VALUES "
            f"({node_id}, '{date}', {x_trend}, {y_trend})"
        )
        total_rows -= 1
        if total_rows % 100 == 0:
            print(f"Remaining rows to insert for node {node_id}: {total_rows}")
    print(f"trend_over_time table updated for node {node_id}.")

    seasonality_df = analyzer.daily_seasonality(table_name, node_id)
    total_rows = len(seasonality_df)
    for hour, row in seasonality_df.iterrows():
        x_mean = row['x']
        y_mean = row['y']
        if pd.isna(x_mean) or pd.isna(y_mean):
            print(f"Skipping insert for node {node_id} on hour {hour} due to NaN value")
            continue
        conn2.execute(
            f"INSERT INTO daily_seasonality VALUES "
            f"({node_id}, {hour}, {x_mean}, {y_mean})"
        )
        total_rows -= 1
        if total_rows % 10 == 0:
            print(f"Remaining rows to insert for node {node_id}: {total_rows}")
    print(f"daily_seasonality table updated for node {node_id}.")

    frequency = analyzer.outlier_frequency(table_name, node_id)
    if frequency is not None:
        conn2.execute(f"INSERT INTO outlier_frequency VALUES ({node_id}, {frequency})")
        print(f"outlier_frequency table updated for node {node_id}.")

    correlation = analyzer.correlation(table_name, node_id)
    if correlation is not None and not math.isnan(correlation):
        conn2.execute(f"INSERT INTO correlation VALUES ({node_id}, {correlation})")
        print(f"correlation table updated for node {node_id}.")

    covariance = analyzer.covariance(table_name, node_id)
    if covariance is not None and not math.isnan(covariance):
        conn2.execute(f"INSERT INTO covariance VALUES ({node_id}, {covariance})")
        print(f"covariance table updated for node {node_id}.")

conn2.commit()
conn2.close()
