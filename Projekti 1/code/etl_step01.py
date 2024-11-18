import csv
import datetime

x_values = [-781, 10406]
y_values = range(0, 5221)
timestamp = datetime.datetime(2019, 3, 31, 10, 10, 10, 123456)

node_id = '0000'
with open('data/results/test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['node_id', 'timestamp', 'x', 'y'])
    for x in x_values:
        for y in y_values:
            writer.writerow([node_id, timestamp, x, y])
    for y in [0, 5220]:
        for x in range(-781, 10406):
            writer.writerow([node_id, timestamp, x, y])

node_id = '0001'
with open('data/results/test.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(0, 541):
        writer.writerow([node_id, timestamp, 10407, y])
    for y in range(0, 541):
        writer.writerow([node_id, timestamp, 8415, y])
    for x in range(8415, 10407):
        writer.writerow([node_id, timestamp, x, 0])
    for x in range(8415, 10407):
        writer.writerow([node_id, timestamp, x, 540])

node_id = '0002'
with open('data/results/test.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(4670, 5221):
        writer.writerow([node_id, timestamp, 10406, y])
    for y in range(4670, 5221):
        writer.writerow([node_id, timestamp, 9890, y])
    for x in range(9890, 10407):
        writer.writerow([node_id, timestamp, x, 4670])
    for x in range(9890, 10407):
        writer.writerow([node_id, timestamp, x, 5221])

node_id = '0003'
with open('data/results/test.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(3250, 5221):
        writer.writerow([node_id, timestamp, 1510, y])
    for y in range(3250, 5221):
        writer.writerow([node_id, timestamp, -781, y])
    for x in range(-781, 1510):
        writer.writerow([node_id, timestamp, x, 3250])
    for x in range(-781, 1510):
        writer.writerow([node_id, timestamp, x, 5221])

node_id = '0004'
with open('data/results/test.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(2965, 3550):
        writer.writerow([node_id, timestamp, 1725, y])
    for y in range(2965, 3550):
        writer.writerow([node_id, timestamp, 240, y])
    for x in range(240, 1725):
        writer.writerow([node_id, timestamp, x, 2965])
    for x in range(240, 1725):
        writer.writerow([node_id, timestamp, x, 3550])

node_id = '0005'
with open('data/results/test.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(2350, 2965):
        writer.writerow([node_id, timestamp, 600, y])
    for y in range(2350, 2965):
        writer.writerow([node_id, timestamp, 900, y])
    for x in range(600, 900):
        writer.writerow([node_id, timestamp, x, 2350])
    for x in range(600, 900):
        writer.writerow([node_id, timestamp, x, 2965])

node_id = '0006'
with open('data/results/test.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(0, 2100):
        writer.writerow([node_id, timestamp, 0, y])
    for y in range(0, 2100):
        writer.writerow([node_id, timestamp, 200, y])
    for x in range(0, 200):
        writer.writerow([node_id, timestamp, x, 0])
    for x in range(0, 200):
        writer.writerow([node_id, timestamp, x, 2100])

node_id = '0007'
with open('data/results/test.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(2350, 3965):
        writer.writerow([node_id, timestamp, -781, y])
    for y in range(2350, 3965):
        writer.writerow([node_id, timestamp, 550, y])
    for x in range(-781, 550):
        writer.writerow([node_id, timestamp, x, 2350])
    for x in range(-781, 550):
        writer.writerow([node_id, timestamp, x, 3965])

node_id = '0008'
with open('data/results/test.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(2150, 2400):
        writer.writerow([node_id, timestamp, -200, y])
    for y in range(2150, 2400):
        writer.writerow([node_id, timestamp, 410, y])
    for x in range(-200, 410):
        writer.writerow([node_id, timestamp, x, 2150])
    for x in range(-200, 410):
        writer.writerow([node_id, timestamp, x, 2400])

node_id = '9999'
with open('data/results/test.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(0, 5220):
        writer.writerow([node_id, timestamp, 0, y])

node_id = '1001'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    writer.writerow(['node_id', 'timestamp', 'x', 'y'])
    for y in range(0, 2350):
        writer.writerow([node_id, timestamp, 10407, y])
    for y in range(0, 2350):
        writer.writerow([node_id, timestamp, 9300, y])
    for x in range(9300, 10407):
        writer.writerow([node_id, timestamp, x, 0])
    for x in range(9300, 10407):
        writer.writerow([node_id, timestamp, x, 2350])

node_id = '1002'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(2450, 3600):
        writer.writerow([node_id, timestamp, 10407, y])
    for y in range(2450, 3600):
        writer.writerow([node_id, timestamp, 9300, y])
    for x in range(9300, 10407):
        writer.writerow([node_id, timestamp, x, 2450])
    for x in range(9300, 10407):
        writer.writerow([node_id, timestamp, x, 3600])

node_id = '1003'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(3750, 5221):
        writer.writerow([node_id, timestamp, 10407, y])
    for y in range(3750, 5221):
        writer.writerow([node_id, timestamp, 6900, y])
    for x in range(6900, 10407):
        writer.writerow([node_id, timestamp, x, 3750])
    for x in range(6900, 10407):
        writer.writerow([node_id, timestamp, x, 5221])

node_id = '1004'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(3750, 5221):
        writer.writerow([node_id, timestamp, 6850, y])
    for y in range(3750, 5221):
        writer.writerow([node_id, timestamp, 1500, y])
    for x in range(1500, 6850):
        writer.writerow([node_id, timestamp, x, 3750])
    for x in range(1500, 6850):
        writer.writerow([node_id, timestamp, x, 5221])

node_id = '1005'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(2350, 3300):
        writer.writerow([node_id, timestamp, 9000, y])
    for y in range(2350, 3300):
        writer.writerow([node_id, timestamp, 6800, y])
    for x in range(6800, 9000):
        writer.writerow([node_id, timestamp, x, 2350])
    for x in range(6800, 9000):
        writer.writerow([node_id, timestamp, x, 3300])

node_id = '1006'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(2350, 3300):
        writer.writerow([node_id, timestamp, 6700, y])
    for y in range(2350, 3300):
        writer.writerow([node_id, timestamp, 3100, y])
    for x in range(3100, 6700):
        writer.writerow([node_id, timestamp, x, 2350])
    for x in range(3100, 6700):
        writer.writerow([node_id, timestamp, x, 3300])

node_id = '1007'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(2350, 3300):
        writer.writerow([node_id, timestamp, 3000, y])
    for y in range(2350, 3300):
        writer.writerow([node_id, timestamp, 2000, y])
    for x in range(2000, 3000):
        writer.writerow([node_id, timestamp, x, 2350])
    for x in range(2000, 3000):
        writer.writerow([node_id, timestamp, x, 3300])

node_id = '1008'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(2350, 2700):
        writer.writerow([node_id, timestamp, 1950, y])
    for y in range(2350, 2700):
        writer.writerow([node_id, timestamp, 550, y])
    for x in range(550, 1950):
        writer.writerow([node_id, timestamp, x, 2350])
    for x in range(550, 1950):
        writer.writerow([node_id, timestamp, x, 2700])

node_id = '1009'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(1150, 2250):
        writer.writerow([node_id, timestamp, 9000, y])
    for y in range(1150, 2250):
        writer.writerow([node_id, timestamp, 7700, y])
    for x in range(7700, 9000):
        writer.writerow([node_id, timestamp, x, 1150])
    for x in range(7700, 9000):
        writer.writerow([node_id, timestamp, x, 2250])

node_id = '1010'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(1150, 2250):
        writer.writerow([node_id, timestamp, 7650, y])
    for y in range(1150, 2250):
        writer.writerow([node_id, timestamp, 6300, y])
    for x in range(6300, 7650):
        writer.writerow([node_id, timestamp, x, 1150])
    for x in range(6300, 7650):
        writer.writerow([node_id, timestamp, x, 2250])

node_id = '1011'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(1150, 2250):
        writer.writerow([node_id, timestamp, 6250, y])
    for y in range(1150, 2250):
        writer.writerow([node_id, timestamp, 5650, y])
    for x in range(5650, 6250):
        writer.writerow([node_id, timestamp, x, 1150])
    for x in range(5650, 6250):
        writer.writerow([node_id, timestamp, x, 2250])

node_id = '1012'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(1250, 2250):
        writer.writerow([node_id, timestamp, 5400, y])
    for y in range(1250, 2250):
        writer.writerow([node_id, timestamp, 2000, y])
    for x in range(2000, 5400):
        writer.writerow([node_id, timestamp, x, 1250])
    for x in range(2000, 5400):
        writer.writerow([node_id, timestamp, x, 2250])

node_id = '1013'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(1250, 2250):
        writer.writerow([node_id, timestamp, 1950, y])
    for y in range(1250, 2250):
        writer.writerow([node_id, timestamp, 1300, y])
    for x in range(1300, 1950):
        writer.writerow([node_id, timestamp, x, 1250])
    for x in range(1300, 1950):
        writer.writerow([node_id, timestamp, x, 2250])

node_id = '1014'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(1350, 2250):
        writer.writerow([node_id, timestamp, 1250, y])
    for y in range(1350, 2250):
        writer.writerow([node_id, timestamp, 600, y])
    for x in range(600, 1250):
        writer.writerow([node_id, timestamp, x, 1350])
    for x in range(600, 1250):
        writer.writerow([node_id, timestamp, x, 2250])

node_id = '1015'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(0, 750):
        writer.writerow([node_id, timestamp, 9250, y])
    for y in range(0, 750):
        writer.writerow([node_id, timestamp, 6250, y])
    for x in range(6250, 9250):
        writer.writerow([node_id, timestamp, x, 0])
    for x in range(6250, 9250):
        writer.writerow([node_id, timestamp, x, 750])

node_id = '1016'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(0, 750):
        writer.writerow([node_id, timestamp, 6200, y])
    for y in range(0, 750):
        writer.writerow([node_id, timestamp, 4400, y])
    for x in range(4400, 6200):
        writer.writerow([node_id, timestamp, x, 0])
    for x in range(4400, 6200):
        writer.writerow([node_id, timestamp, x, 750])

node_id = '1017'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(0, 950):
        writer.writerow([node_id, timestamp, 4350, y])
    for y in range(0, 950):
        writer.writerow([node_id, timestamp, 3000, y])
    for x in range(3000, 4350):
        writer.writerow([node_id, timestamp, x, 0])
    for x in range(3000, 4350):
        writer.writerow([node_id, timestamp, x, 950])

node_id = '1018'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(0, 950):
        writer.writerow([node_id, timestamp, 2950, y])
    for y in range(0, 950):
        writer.writerow([node_id, timestamp, 1750, y])
    for x in range(1750, 2950):
        writer.writerow([node_id, timestamp, x, 0])
    for x in range(1750, 2950):
        writer.writerow([node_id, timestamp, x, 950])

node_id = '1019'
with open('data/results/section.csv', 'a', newline='') as file:  
    writer = csv.writer(file)
    for y in range(0, 950):
        writer.writerow([node_id, timestamp, 600, y])
    for y in range(0, 950):
        writer.writerow([node_id, timestamp, 1750, y])
    for x in range(600, 1700):
        writer.writerow([node_id, timestamp, x, 0])
    for x in range(600, 1700):
        writer.writerow([node_id, timestamp, x, 950])
