from geographiclib.geodesic import Geodesic

geod = Geodesic.WGS84
g = geod.Inverse(10.0, 0.0, 0.0, 10.0)
g1 = geod.Direct(10.0, 0.0, 180-134.37096314105978+270, g['s12']/2)

l = geod.InverseLine(10.0, 0.0, 0.0, 10.0)
g2 = l.Position(l.s13/2)
print(l.s13)
print(g1)
print(g2)