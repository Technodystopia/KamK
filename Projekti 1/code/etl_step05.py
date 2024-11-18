import duckdb

conn = duckdb.connect(database='data/etl.duckdb')

print("Step 0: Filtering data based on condition 0...")
conn.execute('''
    CREATE TABLE IF NOT EXISTS step0 AS
    SELECT *
    FROM original
    WHERE (x BETWEEN 0 AND 10406 AND y BETWEEN 0 AND 5220)
''')
print("Step 0 completed.")

print("Step 1: Filtering data based on condition 1...")
conn.execute('''
    CREATE TABLE IF NOT EXISTS step1 AS
    SELECT *
    FROM step0
    WHERE NOT (x BETWEEN 8415 AND 10407 AND y BETWEEN 0 AND 540)
''')
print("Step 1 completed.")

print("Step 2: Filtering data based on condition 2...")
conn.execute('''
    CREATE TABLE IF NOT EXISTS step2 AS
    SELECT *
    FROM step1
    WHERE NOT (x BETWEEN 9890 AND 10407 AND y BETWEEN 4670 AND 5221)
''')
print("Step 2 completed.")

print("Step 3: Filtering data based on condition 3...")
conn.execute('''
    CREATE TABLE IF NOT EXISTS step3 AS
    SELECT *
    FROM step2
    WHERE NOT (x BETWEEN -781 AND 1510 AND y BETWEEN 3250 AND 5221)
''')
print("Step 3 completed.")

print("Step 4: Filtering data based on condition 4...")
conn.execute('''
    CREATE TABLE IF NOT EXISTS step4 AS
    SELECT *
    FROM step3
    WHERE NOT (x BETWEEN -781 AND 550 AND y BETWEEN 2350 AND 3965)
''')
print("Step 4 completed.")

print("Step 5: Filtering data based on condition 5...")
conn.execute('''
    CREATE TABLE IF NOT EXISTS step5 AS
    SELECT *
    FROM step4
    WHERE NOT (x BETWEEN -200 AND 410 AND y BETWEEN 2150 AND 2400)
''')
print("Step 5 completed.")

print("Step 6: Filtering data based on condition 6...")
conn.execute('''
    CREATE TABLE IF NOT EXISTS step6 AS
    SELECT *
    FROM step5
    WHERE NOT (x BETWEEN 240 AND 1725 AND y BETWEEN 2965 AND 3550)
''')
print("Step 6 completed.")

print("Filtering data based on time...")
conn.execute('''
    CREATE TABLE IF NOT EXISTS time AS
    SELECT *
    FROM step6
    WHERE CAST(timestamp AS TIME) >= TIME '06:00:00'
    AND CAST(timestamp AS TIME) < TIME '23:00:00'
''')
print("Time filtering completed.")

conn.close()

print("Filtered data has been saved.")
