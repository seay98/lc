import math
import csv
import lines

csvpath = "/home/yh/data/35001-145069592.csv"
base = lines.get_wgs84([25.060810, 102.712654])

points = []
with open(csvpath) as cf:
    rd = csv.DictReader(cf)
    for row in rd:
        point = {}
        point['lat'] = row['latitude']
        point['lng'] = row['longitude']
        point['rs'] = row['rs']
        # point: [lat, lon]
        p = [round(float(point['lat']), 6), round(float(point['lng']), 6)]
        # Convert to WGS84
        pw = lines.get_wgs84(p)
        points.append(pw)

# 离基站最远的点
top = lines.find_geomaxdispoint(base, points)
ps = lines.find_geomaxdislinepoint([base, top], points)
for i in range(len(ps)):
    ps[i] = lines.get_gcj02(ps[i])
print(ps)