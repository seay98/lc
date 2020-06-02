import math
import csv
import lines

csvpath = "/home/yh/data/35001-145069592.csv"

def dataclean(csvpath):
    points = []
    with open(csvpath) as cf:
        rd = csv.DictReader(cf)
        # Find points with same rs have the distance of more than a number
        for row in rd:
            point = {}
            point['lat'] = row['latitude']
            point['lng'] = row['longitude']
            point['rs'] = row['rs']
            if point in points:
                continue
            sameloc = False
            for p in points:
                if p['lat'] == point['lat'] and p['lng'] == point['lng'] and int(p['rs']) < int(point['rs']):
                    p['rs'] = point['rs']
                    sameloc = True
            if sameloc:
                continue
            points.append(point)
    return points

validpoints = []
points = dataclean(csvpath)
for point in points:
    for p in points:
        # point: [lat, lon]
        p1 = [round(float(p['lat']), 6), round(float(p['lng']), 6)]
        p2 = [round(float(point['lat']), 6), round(float(point['lng']), 6)]
        # Convert to WGS84
        p1w = lines.get_wgs84(p1)
        p2w = lines.get_wgs84(p2)
        # print(lines.get_geodistance(p1w, p2w))
        if p['rs'] == point['rs'] and lines.get_geodistance(p1w, p2w) > 20.0:
            pp = [p1w, p2w]
            validpoints.append(pp)
    
print(len(validpoints))
# Find points on the line that is perpendicular to the given line
pointsline = []
for vp in validpoints:
    vp1 = vp[0]
    vp2 = vp[1]
    print(vp)
    p4s = lines.find_geoperpendicularpoints(vp1, vp2)
    pointsline.append(p4s)

print(len(pointsline))
# If the distance between two points is less than a number, they may cross
intersections = []
for i in range(len(pointsline)):
    pl1 = pointsline[i]
    for j in range(i+1, len(pointsline)):
        pl2 = pointsline[j]
        intersection = lines.get_geointersection(pl1, pl2)
        if intersection:
            intersections.append(lines.get_gcj02(intersection))
print(intersections)
