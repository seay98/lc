import math
import numpy
from geographiclib.geodesic import Geodesic
import gpstrans

# 地理坐标系找垂直线上的点
def find_geoperpendicularpoints(p1, p2):
    geod = Geodesic.WGS84
    l = geod.InverseLine(p1[0], p1[1], p2[0], p2[1])
    p3 = l.Position(l.s13/2)

    ds = 1000.0
    interval = 10.0
    p4s = []
    for i in range(math.ceil(ds/interval)):
        p4 = geod.Direct(p3['lat2'], p3['lon2'], p3['azi2']-90, i*interval)
        p0 = [p4['lat2'], p4['lon2']]
        p4s.append(p0)

    for i in range(1,math.ceil(ds/interval)):
        p4 = geod.Direct(p3['lat2'], p3['lon2'], p3['azi2']+90, i*interval)
        p0 = [p4['lat2'], p4['lon2']]
        p4s.append(p0)

    return p4s

# 地理坐标系上有可能的交点
def get_geointersection(pl1, pl2, interval=10):
    intersection = []
    mindistpoints = []
    mindist = 9999
    for p1 in pl1:
        for p2 in pl2:
            ds = get_geodistance(p1, p2)
            if ds < mindist:
                mindist = ds
                mindistpoints = [p1, p2]

    if mindistpoints and mindist < interval:
        geod = Geodesic.WGS84
        l = geod.InverseLine(mindistpoints[0][0], mindistpoints[0][1], mindistpoints[1][0], mindistpoints[1][1])
        p0 = l.Position(l.s13/2)
        intersection = [p0['lat2'], p0['lon2']]

    return intersection

# 地理坐标系上离base最远的点
def find_geomaxdispoint(base, points):
    point = []
    maxds = 0
    for p in points:
        ds = get_geodistance(base, p)
        if ds > maxds:
            maxds = ds
            point = p
    return point

# 地理坐标系上离线最远点
def find_geomaxdislinepoint(l, points):
    geod = Geodesic.WGS84
    g = geod.Inverse(l[0][0], l[0][1], l[1][0], l[1][1])
    # p1 = []
    # p2 = []
    maxar1 = g['azi1']
    maxar2 = g['azi1']
    for p in points:
        # gp = geod.Polygon()
        # gp.AddPoint(l[0][0], l[0][1])
        # gp.AddPoint(l[1][0], l[1][1])
        # gp.AddPoint(p[0], p[1])
        # _, _, area = gp.Compute()
        g1 = geod.Inverse(l[0][0], l[0][1], p[0], p[1])
        a1 = g1['azi1']
        if a1 < 0:
            a1 = 360.0 + a1
        if maxar1 < a1:
            maxar1 = a1
            # p1 = p
        elif maxar2 > a1:
            maxar2 = a1
            # p2 = p
    # p1w = geod.Direct(l[0][0], l[0][1], maxar1, g['s12'])
    # p2w = geod.Direct(l[0][0], l[0][1], maxar2, g['s12'])
    num = 4
    n = (maxar2-maxar1) / num
    ps = []
    for i in range(num+1):
        pg = geod.Direct(l[0][0], l[0][1], maxar1+i*n, g['s12'])
        ps.append([pg['lat2'], pg['lon2']])
    return ps


# 地理坐标系距离计算, WGS84, Parameter: (lat, lng)
def get_geodistance(p1, p2):
    geod = Geodesic.WGS84
    g = geod.Inverse(p1[0], p1[1], p2[0], p2[1])
    return round(g['s12'], 3)


# GCJ-02 to WGS84. Parameter: (lng, lat)
def get_wgs84(p):
    pw = gpstrans.gcj02towgs84(p[1], p[0])
    return [pw[1], pw[0]]

# WGS84 to GCJ-02. Parameter: (lng, lat)
def get_gcj02(p):
    pg = gpstrans.wgs84togcj02(p[1], p[0])
    return [pg[1], pg[0]]

# There are p1 and p2, finding p3 and p4.
# 直角坐标系找垂直线
def find_perpendicular(p1, p2):
    p3 = []
    p4=[]
    p3[0] = math.fabs(p1[0] - p2[0])
    p3[1] = math.fabs(p1[1] - p2[1])

    a1 = math.asin(math.fabs(p1[1]-p2[1])/get_geodistance(p1,p2))

    pleft = p1
    if (p1[0] > p2[0]):
        pleft = p2
    p4[1] = pleft[1]
    p4[0] = pleft[0] + (get_geodistance(p1, p2)/2)/math.cos(a1)
    return p3, p4

# 直角坐标系找交点
def find_intersection(l1, l2):
    p = []
    x1=l1[0]
    y1=l1[1]
    x2=l1[2]
    y2=l1[3]
    
    x3=l2[0]
    y3=l2[1]
    x4=l2[2]
    y4=l2[3]

    p[0] = ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) ) 
    p[1] = ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )

    return p

# 直角坐标系向量欧氏距离
def get_distance(p1, p2):
    x = numpy.array(p1)
    y =  numpy.array(p2)
    d = numpy.linalg.norm(x-y)
    return d
    

    