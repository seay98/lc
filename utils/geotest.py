from geographiclib.geodesic import Geodesic
from matplotlib.path import Path
import lines

geod = Geodesic.WGS84
g = geod.Inverse(10.0, 0.0, 10.0, 0.0)
# g1 = geod.Direct(10.0, 0.0, 180-134.37096314105978+270, g['s12']/2)

# l = geod.InverseLine(10.0, 0.0, 0.0, 10.0)
# g2 = l.Position(l.s13/2)

# print(g['s12'])
# ps1 = lines.find_geoperpendicularpoints([10.0,0.0], [9.995,0.0])
# ps2 = lines.find_geoperpendicularpoints([10.0,0.0], [10.0,0.005])
# ps = lines.get_geointersection(ps1, ps2)
# print(ps)

# ps = lines.find_geomaxdislinepoint([[10.0,10.0], [0.0,10.0]], [[5.0,5.0],[5.0,15.0]])
# print(ps)

# pss = lines.get_geocoverpoints([[10.0,10.0], [0.0,10.0], [5.0,5.0],[5.0,15.0]])
# print(pss)

polygon = Path([(10.0,10.0),(10.0,20.0),(5.0,20.0),(5.0,10.0)])
inornot = polygon.contains_point([5.0,15.0])
print(inornot)