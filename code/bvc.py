#from scipy import shape
#from scipy import array
#import scipy
#from scipy.spatial import ConvexHull
#from matplotlib.path import Path
from shapely.geometry import Point, MultiPoint, Polygon, mapping
from math import sin, cos, pi
import random
from itertools import combinations
import matplotlib.pyplot as plt

#p: process, r: round, c: content message
def RbSend(p, r, v):
    return

def RbReceiveWitness(points, f): #produces n - f good points and f bad points with random values
    badPoint = lambda:[random.uniform(-2,2)] * len(points[0])
    #np = points[:]
    #np[:-f] = [badPoint() for x in range(f)]
    badPoints = [badPoint() for x in range(f)]
    return points + badPoints
    #random.shuffle(np)
    # return np[:-f]


def BVC_MH():
    return

def BVC_VG(goodPts, f):
    rounds = []
    rounds.append(RbReceiveWitness(goodPts, f))
    R = CalculateVgRound()
    for r in range(R):
        newPts = []
        for p in range(len(goodPts)+f):
            points = RbReceiveWitness(rounds[r][:-f], f)
            newPt = VG_Round(points, f)
            newPts.append(newPt)
        rounds.append(newPts)
    return rounds

def VG_Round(points, f):
    z = []
    k = len(points) - f
    for subset in combinations(points, k):
        safe = CalculateSafeArea(subset, f)
        z.append(VG_DeterministicallyChoosePoint(safe))
    v = VG_avgPoints(z)
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
    return 5
def CalculateMhRound():
    return 5

def CalculateSafeArea(points, f):
    k = len(points) - f
    area = MultiPoint(points).convex_hull
    for subset in combinations(points, k):
        subarea = MultiPoint(subset).convex_hull
        area = area.intersection(subarea)
    return area

def pcontains(points, point):
    hull = MultiPoint(points).convex_hull
    return hull.contains(point)

points = [(0,0,0),(1,0,0),(0,1,0), (0,0,1)]
print pcontains(points,Point(0.1,0.1,0.1))
print pcontains(points, Point(0,0,0))
print pcontains(points, Point(1,1,1))
print RbReceiveWitness(points, 1)
print RbReceiveWitness(points, 2)

points = [[cos(t), sin(t)] for t in [t * 2 * pi / 5.0 for t in range(5)]]
print points
print CalculateSafeArea(points, 1)

print 'result'
bvc_result = BVC_VG(points, 1)
colors = 'grcmykwgrcmykw'
for round, col in zip(bvc_result, colors[:len(bvc_result)]):
    points = [Point(xy) for xy in round]
    avgPnt = VG_avgPoints(points)
    xcoords = [xy[0] for xy in round]
    ycoords = [xy[1] for xy in round]
    plt.plot(xcoords, ycoords, col+'o')
    plt.plot([avgPnt[0]],[avgPnt[1]], 'bx')
    plt.axis([-1, 1, -1, 1])

plt.show()

#POLYGON ((0.309 -0.225, -0.118 -0.363, -0.382 0, -0.118 0.363, 0.309 0.225, 0.309 -0.225))