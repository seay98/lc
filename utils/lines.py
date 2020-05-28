import math
import numpy
from geographiclib.geodesic import Geodesic
import gpstrans

# 地理坐标系找垂直线上的点
def find_geoperpendicularpoints(p1, p2):
    geod = Geodesic.WGS84
    l = geod.InverseLine(p1[0], p1[1], p2[0], p2[1])
    p3 = l.Position(l.s13/2)

    ds = 100
    interval = 5
    p4s = []
    for i in range(ds/interval):
        p4 = geod.Direct(p3['lat2'], p3['lon2'], p3['azi2']-90, i*interval)
        p0 = [p4['lat2'], p4['lon2']]
        p4s.append(p0)

    for i in range(ds/interval):
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


# 地理坐标系距离计算, WGS84, Parameter: (lat, lng)
def get_geodistance(p1, p2):
    geod = Geodesic.WGS84
    g = geod.Inverse(p1[0], p1[1], p2[0], p2[1])
    return round(g['s12'], 2)


# GCJ-02 to WGS84. Parameter: (lng, lat)
def get_wgs84(p):
    return gpstrans.gcj02towgs84(p[1], p[0])

# WGS84 to GCJ-02. Parameter: (lng, lat)
def get_gcj02(p):
    return gpstrans.wgs84togcj02(p[1], p[0])

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
    

    