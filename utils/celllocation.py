import math
import csv
import lines

csvpath = "/home/yh/data/3467-14597381.csv"

with open(csvpath) as cf:
    rd = csv.DictReader(cf)
    points = []
    validpoints = []
    for row in rd:
        point = {}
        point['lat'] = row['latitude']
        point['lng'] = row['longitude']
        point['rs'] = row['rs']
        points.append(point)
        for p in points:
            p1 = [float(p['lat']), float(p['lng'])]
            p2 = [float(point['lat']), float(point['lng'])]
            if p['rs'] == point['rs'] and lines.get_geodistance(p1, p2) > 20.0:
                validpoints.append(p)
                validpoints.append(point)
    
print(len(validpoints))
