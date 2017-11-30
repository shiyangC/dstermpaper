from shapely.geometry import Point, MultiPoint, Polygon, mapping
from math import sin, cos, pi
import random
import matplotlib.pyplot as plt

import bvc

points = [[round(cos(t),1), round(sin(t),1)] for t in [t * 2 * pi / 5.0 for t in range(5)]]
plt.axes().set_aspect(1)
newPts = points
#newPts = bvc.RbReceiveWitness(points, 1)
#bvc.plotPolyXY(newPts, color='black', linewidth=1)
hull = MultiPoint(newPts).convex_hull
hull = bvc.hullToPts(hull)
bvc.plotPolyXY(hull, color='blue', linewidth=2)
print hull
safe = bvc.CalculateSafeArea(hull, 1)
bvc.plotPoly(safe, color='red', linewidth=1)
plt.show()

