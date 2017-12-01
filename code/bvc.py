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
    badPoint = lambda:tuple([round(1.5 * random.uniform(-1,1),2) for i in range(len(points[0]))])
    #np = points[:]
    #np[:-f] = [badPoint() for x in range(f)]
    badPoints = [badPoint() for x in range(f)]
    print "badPoints" , badPoints
#   for bp in badPoints:
#        plt.plot(bp, 'rx')
    return points + badPoints
    #random.shuffle(np)
    # return np[:-f]


def BVC_MH(goodPts, f):
    plotPoly(Polygon(goodPts), color='black', linewidth=2)
    plotPoly(CalculateSafeArea(goodPts,f), color='blue', linewidth=2)
    colors = 'rcygbkp'

    R = 2 #CalculateMhRound()

    n = len(goodPts) + f
    rounds = [[(0, 0)] * n] * (R + 1)
    rounds[0] = RbReceiveWitness(goodPts, f)

    d = len(goodPts[0])
    for m in range(d):
        for rIdx in range(1,R+1):
            H = [0] * n #halt msg received in each process
            r = [1] * n #round in each process
            if rIdx == 2:
                a=1+1
            for p in range(n):
                #while H[p] <= f:  #assume H received immedately
                    #RbSend()
                    points = RbReceiveWitness(rounds[rIdx-1][:-f],f)
                    safe = CalculateSafeArea(points, f)
                    v = MH_DeterministicallyChoosePoint(safe, m)
                    rounds[rIdx][p] = v
                    if r[p] == R:
                        H = [c+1 for c in H]
                    r[p] = r[p]+1

                #RbReceive
                #for p in range(n):
                    # can deduct some of H to simulate delayed received halt msgs?

    for round in rounds:
        plotPoly(ptsToHull(round), color='blue', linewidth=1)
    return rounds

def MH_DeterministicallyChoosePoint(safeAreaPgon, dim):
#    if safeAreaPgon.geom_type == "LineString":
#        x,y = safeAreaPgon.centroid.xy
#        return [x,y]
    points = polyToPts(safeAreaPgon)
    points.sort(key=lambda p:p[dim])
    midpoint = points[len(points)/2]
    return midpoint

def BVC_VG(goodPts, f):
    plotPoly(Polygon(goodPts), color='black', linewidth=2)
    plotPoly(CalculateSafeArea(goodPts,f), color='blue', linewidth=2)
    colors = 'rcygbkp'
    rounds = []
    rounds.append(RbReceiveWitness(goodPts, f))
    plotPoly(ptsToHull(rounds[0]), linewidth=1)
    R = CalculateVgRound()
    for r in range(R):
        newPts = []
        for p in range(len(goodPts)+f):
            points = RbReceiveWitness(rounds[r][:-f], f)
            newPt = VG_Round(points, f)
            newPts.append(newPt)
        rounds.append(newPts)
        plotPoly(ptsToHull(newPts), color=colors[r], linewidth=1)
    return rounds

def VG_Round(points, f):
    z = []
    k = len(points) - f
    sets = list(combinations(points, k))
    random.shuffle(sets)
    sets = sets[:len(points)]
    for subset in sets:
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
        #print subset
        subarea = MultiPoint(subset).convex_hull
        area = area.intersection(subarea)
    return area

def pcontains(points, point):
    hull = MultiPoint(points).convex_hull
    return hull.contains(point)

def ptsToPoly(points):
    return Polygon(points)
def polyToPts(poly):
    try:
        x,y = poly.exterior.xy
    except:
        x = [poly.bounds[0], poly.bounds[2]]
        y = [poly.bounds[1], poly.bounds[3]]

    l = zip(x,y)
    q = set()
    r = []
    for t in l:
        if t not in q:
            q.add(t)
            r.append(t)
    return r
def ptsToHull(points):
    return MultiPoint(points).convex_hull
def polyToHull(poly):
    return ptsToHull(ptsToPoly(poly))
def hullToPts(hull):
    return polyToPts(hull)
def hullToPoly(hull):
    return Polygon(hull)

def plotPoly(poly,name='fig 1', color='#6699cc', alpha=0.7, linewidth=1, zorder=2):
    x,y = poly.exterior.xy
    plt.plot(x,y,color=color, alpha=alpha, linewidth=linewidth, zorder=zorder)
    plt.title(name)
#    plt.show()
    return

def plotPolyXY(points, name='fig 1', color='#6699cc', alpha=0.7, linewidth=1, zorder=2):
    plotPoly(Polygon(points), name=name, color=color, alpha=alpha, linewidth=linewidth, zorder=zorder)

def plotPoints(points, name='fig 1', color='#6699cc', alpha=0.7, linewidth=1, zorder=2):
    x = [xy[0] for xy in points]
    y = [xy[1] for xy in points]
    plt.plot(x,y,color=color, alpha=alpha, linewidth=linewidth, zorder=zorder)
    plt.title(name)
#    plt.show()
    return

if __name__ == "__main__":
    # points = [(0,0,0),(1,0,0),(0,1,0), (0,0,1)]
    # print pcontains(points,Point(0.1,0.1,0.1))
    # print pcontains(points, Point(0,0,0))
    # print pcontains(points, Point(1,1,1))
    # print RbReceiveWitness(points, 1)
    # print RbReceiveWitness(points, 2)

    n = 7
    f = 2
    points = [[round(cos(t),2), round(sin(t),2)] for t in [t * 2 * pi / n for t in range(n)]]
#    print points
#    print CalculateSafeArea(points, 1)

    print 'result'
    bvc_result = BVC_VG(points, f)
#    bvc_result = BVC_MH(points, 1)

    plt.axes().set_aspect(1)
    plt.show()


#POLYGON ((0.309 -0.225, -0.118 -0.363, -0.382 0, -0.118 0.363, 0.309 0.225, 0.309 -0.225))