from geographiclib.geodesic import Geodesic
import lines

geod = Geodesic.WGS84
g = geod.Inverse(9.995, 0.0, 10.0, 0.005)
# g1 = geod.Direct(10.0, 0.0, 180-134.37096314105978+270, g['s12']/2)

# l = geod.InverseLine(10.0, 0.0, 0.0, 10.0)
# g2 = l.Position(l.s13/2)

print(g['s12'])
ps1 = lines.find_geoperpendicularpoints([10.0,0.0], [9.995,0.0])
ps2 = lines.find_geoperpendicularpoints([10.0,0.0], [10.0,0.005])
ps = lines.get_geointersection(ps1, ps2)
print(ps)