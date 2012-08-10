#!/usr/bin/python

import time
from math import log

#Problem 169
#April 19, 2012
#Solved May 7th, 2012

"""
Define f(0) = 1 and f(n) to be the number of different ways n can be
expressed as a sum of integer powers of 2 using each power no more than
twice.  For example f(10) = 5 since there are five different ways to
express 10.  What is f(10^25)?
"""


"""
I went through multiple algorithms to solve this problem.  They all rely on
splitting the target number into the series of powers of two that form the
number.

The first was a recursive solution that brute forced ways.  The second was a
more efficient iterative algorithm that tracked only the powers used.  Neither
of these scaled well as the number of solutions for 10^25 is on the order of
billions.

After playing with the numbers on paper a third, extremely efficient algorithm
was discovered.  It tracks the number of ways of forming the current sum out
of powers of two that have been used so far.  It does this by keeping count of
the number of ways that the sum is formed using the largest exponent.  Then,
each additional higher power expands the number of ways.  Because each power
of two can only be used twice, each way of forming the number must use the
closest, or second closest, power of two.  Thus these are the only numbers
that must be tracked.  The expansion of each way of forming the number is
directly proportional to the difference in the current power and the previous
power of two being considered.
"""


powers = {}

def solve(n):
    global powers
    powers[1] = [(1,)]
    for i in xrange(1, int(log(n, 2)) + 1):
        p = 2**i
        powers[p] = []
        for c in powers[p/2]:
            new = list(c) + [0]
            new[i-1] += 1
            powers[p].append(tuple(new))
        powers[p].append(tuple([0]*i + [1]))

    s = split(n)
    """
    for l in s:
        d = [0]*len(l)
        for i in xrange(len(l)):
            d[i] = l[i]*2**i
        print l, d
    """
    return len(s)

def split(n):
    if n in powers:
        return powers[n]
    else:
        #Split
        a = 2**int(log(n, 2))
        blist = split(n-a)
        
        #Rejoin
        joined = {}
        for m in powers[a]:
            for n in blist:
                new = list(m)
                valid = True
                for i in xrange(len(n)):
                    if m[i] + n[i] > 2:
                        valid = False
                        break
                    else:
                        new[i] += n[i]
                if valid:
                    joined[tuple(new)] = True
        return joined.keys()

    
def solve2(n):
    
    exps = []
    while n:
        e = int(log(n,2))
        n -= 2**e
        exps.append(e)
    print exps
    s = exps.pop()
    #Start expontent with left and right padding
    if exps:
        w = [0]*s + [1] + [0]*(exps[0]-s)
    else:
        return s+1 #n = 2**k for some k
    ways = []
    ways.append(w[:])
    for i in xrange(s, 0, -1):
        w[i] -= 1
        w[i-1] = 2
        ways.append(w[:])
    
    currentsum = 2**s
    for p in reversed(exps):
        start = int(log(currentsum, 2))
        currentsum += 2**p
        #Set up the ways to make the current power p
        w = [0]*p + [1]
        n = {}
        for i in xrange(p, 0, -1):
            w[i] -= 1
            w[i-1] = 2
            n[i-1] = w[:]

        #Expand each way to include the next higher power p
        for x in xrange(len(ways)):
            m = ways[x]
            for i in xrange(start, p):
                if m[i] == 0:
                    new = m[:]
                    for k in xrange(p+1):
                        new[k] += n[i][k]
                    ways.append(new)
            #Add 2**p to each original way
            ways[x][p] = 1
    """
    for y in ways:
        print y
    """
    return len(ways)


def solve3(n):
    exps = []
    while n:
        e = int(log(n,2))
        n -= 2**e
        exps.append(e)
    print exps
    c0 = 1
    c1 = exps.pop()
    largest_power = c1

    for p in reversed(exps):
        c0new = c0
        c1new = c0*(p - largest_power -1)

        c0new += c1
        c1new += c1*(p - largest_power)

        largest_power = p

        c0 = c0new
        c1 = c1new

    return c0 + c1



if __name__ == "__main__":

    t0 = time.clock()

    n = 10**25
    print solve3(n)

   
    print time.clock() - t0, "seconds process time"
