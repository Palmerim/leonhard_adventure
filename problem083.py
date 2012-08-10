#!/usr/bin/python

import sys
import time
import csv
#Problem 83
#November 10, 2011

"""
NOTE: This problem is a significantly more challenging version of Problem 81.

In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by
moving left, right, up, and down, is indicated in bold red and is equal to 2297.
	
131	673	234	103	18
201	96	342	965	150
630	803	746	422	111
537	699	497	121	956
805	732	524	37	331
	
Find the minimal path sum, in matrix.txt, a 31K text file containing an 80 by 80 matrix.
"""


"""
This solution uses the A* search algorithm to navigate the matrix.  The matrix file is read
into the graph object.  The search heuristic is the number of spaces from the current node to
the goal node.  This is admissible because the optimal path cost will never be less than this
distance.
"""


class Node:
#Node has coordinates (x,y) and cost of visiting the node
    f = 0
    parent = None
    visited = False
    openset = False

    def __init__ (self, x=0, y=0, cost=0, d=1, g=9999):
        self.x = x
        self.y = y
        self.cost = cost
        self.h = 2*(d - 1) - y - x #Number of spaces from goal
        self.g = g

class Graph(Node):
    def __init__ (self, d=0):
        self.start = Node(-1, -1, 0, d, 0)
        self.grid = [[0 for i in xrange(d)] for j in xrange(d)]
        self.d = d

    def get_neighbors(self, n):
        neighbors = []
        i = n.x
        j = n.y
        if n == self.start:
            neighbors = [self.grid[0][0]]
        else:
            if i > 0:
                neighbors.append(self.grid[i-1][j])
            if j > 0:
                neighbors.append(self.grid[i][j-1])
            if i < self.d-1:
                neighbors.append(self.grid[i+1][j])
            if j < self.d-1:
                neighbors.append(self.grid[i][j+1])
        return neighbors

def astar(graph):
"""
A* search algorithm uses priority queue and informed search heuristic h.
"""
    openset = [graph.start]
     
    while openset:
        a = openset.pop(0)
        if a.h == 0: #If a is a goal node
            path = []
            while a.parent: #Reconstruct the path by following the parents
                path.append(a)
                a = a.parent
            return reversed(path)
        else:
            a.visited = True
            for b in graph.get_neighbors(a):
                if not b.visited:
                    tentative_g = a.g + b.cost
                    if not b.openset:
                        b.openset = True
                        openset.append(b)
                        tentative_better = True
                    elif tentative_g < b.g:
                        tentative_better = True
                    else:
                        tentative_better = False
                    if tentative_better:
                        b.parent = a
                        b.g = tentative_g
                        b.f = b.g + b.h
            openset.sort(key = lambda z: z.f)


if __name__ == "__main__":

    t0 = time.clock()
    if len(sys.argv) < 2:
        print "Usage:", sys.argv[0], "GRAPH"
        sys.exit()
    r = csv.reader(open(sys.argv[1], 'r'))
    c = [[int(e) for e in l] for l in r]
    
    d = len(c)
    
    graph = Graph(d)
    for x in xrange(d):
        for y in xrange(d):
            graph.grid[x][y] = Node(x, y, c[x][y], d)
    
    p = astar(graph)

    tot = 0
    for i in p:
        #print i.cost
        tot += i.cost
    print "Route cost:", tot
    
    print time.clock() - t0, "seconds process time"
