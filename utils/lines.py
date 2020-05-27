import math
import numpy
from geographiclib.geodesic import Geodesic
import gpstrans

# There are p1 and p2, finding p3 and p4.
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


def get_geodistance(p1, p2, gcj02=True):
    gps1 = [p1[0], p1[1]]
    gps2 = [p2[0], p2[1]]
    if gcj02:
        gps1 = gpstrans.gcj02towgs84(p1[0], p1[1])
        gps2 = gpstrans.gcj02towgs84(p2[0], p2[1])

    geod = Geodesic.WGS84
    g = geod.Inverse(gps1[0], gps1[1], gps2[0], gps2[1])
    print(round(g['s12'], 2))
    return round(g['s12'], 2)

def get_distance(p1, p2):
    x = numpy.array(p1)
    y =  numpy.array(p2)
    d = numpy.linalg.norm(x-y)
    return d
    

    