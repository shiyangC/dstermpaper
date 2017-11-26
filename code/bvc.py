#from scipy import shape
#from scipy import array
#import scipy
#from scipy.spatial import ConvexHull
#from matplotlib.path import Path
from shapely.geometry import Point, MultiPoint, Polygon, mapping

from math import sin, cos, pi

import random
from itertools import combinations

#p: process, r: round, c: content message
def RbSend(p, r, v):
    return

def RbReceiveWitness(points, f):
    badPoint = [-1] * len(points[0])
    np = points[:]
    np[:f] = [badPoint for x in range(f)]
    return np
    # random.shuffle(np)
    # return np[:-f]


def BVC_MH():
    return

def BVC_VG(points, f):
    #init procs here
    rounds = []
    rounds.append(points)
    R = CalculateVgRound()
    for r in range(R):
        points = RbReceiveWitness(rounds[r], f)
        newPts = VG_Round(points, f)
        rounds.append(newPts)
    return rounds

# every process will run this. But since every process has the same input because of RbReceive, just one process is enough
def VG_Round(points, f):
    z = []
    k = len(points) - f
    for subset in combinations(points, k):
        safe = CalculateSafeArea(subset, f)
        z.append(VG_DeterministicallyChoosePoint(safe))
    v = VG_avgPoints(z) #this part is broken. I don't understand how v will be different for every non-faulty process,
    # since RBReceiveWitness should guarantee that every process receives the same message?
    return v

def VG_DeterministicallyChoosePoint(safeArea):
    return safeArea.centroid

def VG_avgPoints(points):
    dim = 2
    if points[0].has_z:
        dim = 3

    avg=[0] * dim
    avg[0] = sum([p.x for p in points])/len(points)
    avg[1] = sum([p.y for p in points])/len(points)
    if (dim == 3):
        avg[2] = sum(p.z for p in points) / len(points)
    return avg

def CalculateVgRound():
    return 10
def CalculateMhRound():
    return 10

def CalculateSafeArea(points, f):
    k = len(points) - f
    area = MultiPoint(points).convex_hull
    for subset in combinations(points, k):
        subarea = MultiPoint(subset).convex_hull
        area = area.intersection(subarea)
    return area

# def pcontains(points, point):
#     points = array(points, float)
#     hull = ConvexHull(points)
#     hull_path = Path(points[hull.vertices])
#     return hull_path.contains_point(point)

def pcontains(points, point):
    hull = MultiPoint(points).convex_hull
    return hull.contains(point)

points = [(0,0,0),(1,0,0),(0,1,0), (0,0,1)]
print pcontains(points,Point(0.1,0.1,0.1))
print pcontains(points, Point(0,0,0))
print pcontains(points, Point(1,1,1))
print RbReceiveWitness(points, 1)
print RbReceiveWitness(points, 2)

points = [(-10, -10)] + [(cos(t), sin(t)) for t in [t * 2 * pi / 5.0 for t in range(5)]]
print points
print CalculateSafeArea(points, 1)

print BVC_VG(points, 1)

#POLYGON ((0.309 -0.225, -0.118 -0.363, -0.382 0, -0.118 0.363, 0.309 0.225, 0.309 -0.225))