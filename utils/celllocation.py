import math
import csv
import lines

csvpath = "/home/yh/data/3467-14597381.csv"

validpoints = []
with open(csvpath) as cf:
    rd = csv.DictReader(cf)
    points = []
    # Find points with same rs have the distance of more than a number
    for row in rd:
        point = {}
        point['lat'] = row['latitude']
        point['lng'] = row['longitude']
        point['rs'] = row['rs']
        points.append(point)
        for p in points:
            p1 = [float(p['lat']), float(p['lng'])]
            p2 = [float(point['lat']), float(point['lng'])]
            # Convert to WGS84
            p1w = lines.get_wgs84(p1)
            p2w = lines.get_wgs84(p2)
            if p['rs'] == point['rs'] and lines.get_geodistance(p1w, p2w) > 20.0:
                pp = [p1w, p2w]
                validpoints.append(pp)
    
# print(len(validpoints))
# Find points on the line that is perpendicular to the given line
pointsline = []
for vp in validpoints:
    vp1 = vp[0]
    vp2 = vp[1]
    p4s = lines.find_geoperpendicularpoints(vp1, vp2)
    pointsline.append(p4s)

# If the distance between two points is less than a number, they may cross
intersections = []
for i in range(len(pointsline)):
    pl1 = pointsline[i]
    j = i + 1
    for j in range(len(pointsline)):
        pl2 = pointsline[j]
        intersection = lines.get_geointersection(pl1, pl2)
        if intersection:
            intersections.append(intersection)

print(intersections)
