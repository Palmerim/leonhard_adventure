#!/usr/bin/python

import time
from sys import argv
#from math import sqrt
#from operator import itemgetter
#from fractions import gcd
#from fractions import Fraction

#Problem 373
#Started February 29, 2012
#Finished April 12, 20012

"""
Every triangle has a circumscribed circle that goes through the three
vertices. Consider all integer sided triangles for which the radius of the
circumscribed circle is integral as well.

Let S(n) be the sum of the radii of the circumscribed circles of all such
triangles for which the radius does not exceed n. 
"""


"""
Wow, what a ride. Even the problem statement is interesting.

This problem was solved in many stages and different solving versions.  
Overall they can be divided into two stages.  At first, thinking the problem
depended on triangles, specifically Hero or Heronian triangles (those with
rational sides and rational area).  This involved trying to find all Heronian
triangles and scaling them up to be integer sided.  This started with brute
forcing all integer triangle sides, but this was quickly replaced with two
different parameterizations of Heronian triangles found from research.

However these methods were still too slow.  Further research led to the
discovery that all Heronian triangles are either right triangles, or can be
formed by combining two right triangles along a common side.  This produced a
much faster algorithm, however, still not fast enough to reach to n = 10^7.

Then the great realization that the radii were all hypotenuse numbers, numbers
whose squares are the sum of two distinct non-zero squares. This caused a
paradigm shift away from thinking of the problem in terms of triangles, toward
thinking about numbers and their factorization.  These hypotenuse numbers were
also numbers that had at least one prime factor equal to 4k + 1.  Solving the
problem then turned to finding out how many different triangles had the same
circumscribing circle radius.  For example, 5 different triangles have a
radius equal to 25.  This involved going back to the hypotenuse numbers.

Finding all of the ways to form the hypotenuse numbers led to how many
different triangles could have the same circumscribing radius.  This number
was also directly dependent on the form of the prime factorization of the
hypotenuse number.  A number with only one prime factor of the form 4k + 1
had only one triangle with that circumscribing radius.  Wheres numbers with
multiple and repeated factors had more associated triangles.  The shocking
thing about this was that the number of triangles for a given radius was
dependent only on the number of prime factors of the form 4k + 1 and not
on what the factors actually were.  This led to the discovery of two integer
sequences which closed form solutions for triangles with n different and n
same prime factors of their radius.

This led to changing the problem into finding all the factorizations of all
hypotenuse numbers up to n.  And also tracking the number of different
triangles associated with each set of counts of the prime factors 4k + 1.
However, because only a subset of the prime factors contributed to multiple
triangles, the complete factorization of the hypotenuse numbers was not
necessary.

Further research found that a modified version of the Sieve of Eratosthenes
can be used to factor numbers.  The sieve is changed to mark numbers as not
prime by storing their largest prime factor.  Then to factor a number this
table can be used to repeatedly lookup and reduce the number while saving
the factors.  This is much faster than trial division, especially when
factoring many numbers.  Combining this information led to a much simpler
solution that was orders of magnitude faster (in the spirit of Project Euler).
"""

def solve8(limit):
    #Generate hypotenuse numbers up to limit
    phns, table = generate_prime_hypotenuse_numbers(limit+1)
    total = 0
    stored = {}

    for i in xrange(1, 11): #5^10
        stored[(i,)] = int((i + 0.25)**2)
    for i in xrange(1, 7): #5 * 13 * 17 * 29 * 37* 41
        stored[(tuple([1]*i))] = (2*7**i - 3*3**i + 1)/6
        
    for r in xrange(limit+1):
        if table[r] > 0:
            #Only one triangle is associated with a prime radius
            if r == table[r]:
                total += r
            #The number of triangles depends on the number of prime factors
            #of the form 4k+1
            else:  
                counts = factor_hypotenuse(r, table)
                if not (counts in stored):
                    stored[counts] = find_triangle(r)
                total += (r * stored[counts])
    print "v8", limit, total


#Faster Sieve
def generate_prime_hypotenuse_numbers(limit):
    p_array = [x % 4 for x in xrange(limit)]
    pm_array = [0]*limit
    for n in xrange(3, int(limit**0.5)+ 1, 2):
        for i in xrange(2*n, limit, n):
                p_array[i] = 0
    primes = []
    for i in xrange(5, limit, 2):
        if p_array[i] == 1:
            #primes.append(i)
            for j in xrange(i, limit, i):
                pm_array[j] = i
    return primes, pm_array

def factor_hypotenuse(n, table):
    counts = []
    c = 1
    factor = table[n]
    while table[n]:
        n = n/table[n]
        if table[n] == factor:
            c += 1
        else:
            counts.append(c)
            factor = table[n]
            c = 1
    counts.sort()
    return tuple(counts)

def generate_sides(r):
    r2 = r**2
    sides = [2*r]
    for a in xrange(1, int(r/sqrt(2))+1):
        b = sqrt(r2 - a**2)
        if b % 1 == 0:
            b = int(b)
            #print a, b
            sides.append(2*a)
            sides.append(2*b)
    sides.sort()
    return sides

def find_triangle(r):
    """
    Using all possible side lengths, form triangles having a certain
    circumscribing radius.  Return the number of triangles.
    """
    tris = {}
    lengths = generate_sides(r)
    l = len(lengths)
    for i in xrange(l-1):
        for j in xrange(i, l):
            for k in xrange(j, l):
                a, b, c = lengths[i], lengths[j], lengths[k]
                y = (a+b-c)*(a-b+c)*(b+c-a)*(a+b+c)
                if y > 0:
                    if abs(r - a*b*c/sqrt(y)) < 0.0000001:
                        tris[(a, b, c)] = True
    return len(tris.keys())

if __name__ == "__main__":

    t0 = time.clock()

    solve8(int(argv[1]))

    print time.clock() - t0, "seconds process time"




"""
#Faster Sieve April 2012
def generate_primes(limit):
    p_array = [x % 2 for x in xrange(limit)]
    s_max = int(limit**0.5)
    for n in xrange(3, s_max + 1, 2):
        for i in xrange(2*n, limit, n):
                p_array[n] = 0
    primes = []
    p_array[1] = 0
    p_array[2] = 1
    for i in xrange(2, limit):
        if p_array[i] == 1:
            primes.append(i)
    return primes, p_array



#Trial Division
def factorize(n, primes, p_array):
    if n == 1: return [1]
    if p_array[n]:
        return [n]
    factors = []

    for p in primes:
        if p*p > n: break
        while n % p == 0:
            factors.append(p)
            n //= p
    if n > 1: factors.append(n)
    return factors

def solve(limit):
    max_p = 5.2 * limit
    a = 2
    total = 0
    d = []
    iters = 0
    tris = []
    while a <= 1.6*limit:
        count = 0
        b = a
        c = a
        r = 0
        while a+b+c < max_p:
            #Degenerate 
            if r > limit or a + b - c == 0:
                b += 2
                c = b
            
            r = a*b*c/sqrt((a+b-c)*(a-b+c)*(b+c-a)*(a+b+c))
            iters += 1
            #print a, b, c, r, (a+b+c) % 4
            if r % 1 == 0 and r <= limit:
                t = (a, b, c)
                new = True
                for p in d:
                    if t[0] % p[0] == 0 and t[1] % p[1] == 0 \
                        and t[2] % p[2] == 0:
                        new = False
                        break
                if new: d.append(t)
                right = a**2 + b**2 == c**2 
                r = int(r)
                if True:
                    tris.append((t,r))

                total += r
            c += 2 
        a += 2
    for e in sorted(tris, key = lambda x: (x[1])):
        s = sum(e[0])/2.0
        a = sqrt(s*(s-e[0][0])*(s-e[0][1])*(s-e[0][2]))
        print e
    print total
    print iters

def solve2(limit):
    d = {}
    total = 0
    maxn = 0

    for p in xrange(1, limit/100+3):
        p2 = p**2
        for q in xrange(1, limit/100+3):
            gcd1 = gcd(p,q)
            if gcd1 > 1: continue

            q2 = q**2
            x = 4*p*q
            for m in xrange(1, limit/20+35):
                gcd2 = gcd(gcd1,m)
                if gcd2 > 1: continue

                m2 = m**2
                for n in xrange(1, m-3):
                    if gcd(gcd2,n) > 1: continue

                    n2 = n**2
                    r = (p2 + q2)*((p2*m2) + (q2*n2))

                    a = x*m*n*(p2 + q2)
                    b = x*((m2*p2) + (n2*q2))
                    c = x*(m+n)*abs(m*p2 - n*q2)

                    if a > 0 and b > 0 and c > 0:
                        g = gcd(c,r)
                        if g > 1:
                            g = gcd(a, gcd(b, g))
                        if r/g <= limit:

                            sides = [a/g,b/g,c/g]
                            sides.sort()
                            s = (sides[0], sides[1], sides[2], r/g)
                            if s in d:
                                continue
                            #print p, q, m, n
                            #if m > maxn:
                            #    maxn = m

                            #All larger similar triangles
                            h = 1
                            while h*s[3] <= limit:
                                hs = (h*s[0], h*s[1], h*s[2], h*s[3])
                                if not (hs in d):
                                    d[hs] = True
                                    total += hs[3]
                                h += 1

    #for e in sorted(d.keys(), key=itemgetter(3,0)):
    #    print e
    print 'v2', limit, total
   
def solve3(limit):
    ps, pa = generate_primes(2*limit)

    iterlimit = limit/10+50
    klimit = limit/15 + 25
    d = {}
    total = 0
    ln = 0
    lm = 0
    lk = 0

    for m in xrange(1, iterlimit+1):
        m2 = m**2
        for n in xrange(1, m+1):
            n2 = n**2

            for k in xrange(1, klimit+1):
                k2 = k**2

                a = n*(m2 + k2)
                b = m*(n2 + k2)
                c = (m+n)*(m*n - k2)
                
                if a > 0 and b > 0 and c > 0:
                    r = a*b*c/sqrt((a+b-c)*(a-b+c)*(b+c-a)*(a+b+c))
                    if r % 1 == 0:
                        r = int(r)
                        g = gcd(c,r)
                        if g > 1:
                            g = gcd(a, gcd(b, g))
                        if r/g <= limit:
                            sides = [a/g,b/g,c/g]
                            sides.sort()
                            s = (sides[0], sides[1], sides[2], r/g)
                            if s in d:
                                continue
                            #if s[0]**2 + s[1]**2 == s[2]**2:
                            #    print s
                            if m > lm: lm = m
                            if n > ln: ln = n
                            if k > lk: lk = k
                            #All larger similar triangles
                            h = 1
                            while h*s[3] <= limit:
                                hs = (h*s[0], h*s[1], h*s[2], h*s[3])
                                if not (hs in d):
                                    d[hs] = True
                                    total += hs[3]
                                h += 1
    last = 0
    count = 1
    for e in sorted(d.keys(), key=itemgetter(3,0,1)):
        if e[3] == last:
            count += 1
            print e, factorize(e[3], ps, pa), count
        else:
            print ""
            count = 1
            last = e[3]
            print e, factorize(e[3], ps, pa), count
    print 'v3', limit, total, iterlimit, klimit, lm, ln, lk


def solve6(limit):
    ps, pa = generate_primes(2*limit)

    used = {}
    T = []
    total = 0
    r = 0
    u = 1
    #Right triangles, all are Heronian
    while r <= limit:
        for v in xrange(1, u):
            if gcd(u,v) > 1 or (u-v) % 2 == 0:
                continue
            s = sorted([u**2 + v**2, u**2 - v**2, 2*u*v])
            r = s[2]/2.0
            if r <= limit/2:
                T.append(s) 

            #All larger similar triangles
            h = 1
            while h*r <= limit:
                if h*r % 1 == 0:
                    hs = (h*s[0], h*s[1], h*s[2], int(h*r))
                    if not (hs in used):
                        used[hs] = True
                        total += hs[3]
                h += 1
        u += 1
    #for e in sorted(used.keys(), key=itemgetter(3,0,1)):
    #    print e
    #Find non-right Heronian triangles
    for a in T:
        for b in T:
            if b[2] < a[2] or (a[2]+b[2]) > 1.2*limit: continue
            for i in [0, 1]:
                for j in [0, 1]:
                    l = a[i]*b[j]/gcd(a[i], b[j])
                    #if l <= 4*M:
                    if True:
                        x1 = l/a[i]
                        x2 = l/b[j]

                        A = [x1*s for s in a]
                        B = [x2*s for s in b]
                        
                        ni = (i + 1) % 2
                        nj = (j + 1) % 2
                        s = sorted([A[ni]+B[nj], A[2], B[2]])
                        
                        Area = 0.5*(A[0]*A[1] + B[0]*B[1])
                        r = s[0]*s[1]*s[2]/(4*Area)
                        F = Fraction.from_float(r).limit_denominator()
                        D = F.denominator
                        #print a, x1, A
                        #print b, x2, B
                        #print s, r, F
                        s = (D*s[0], D*s[1], D*s[2], F.numerator)
                        g = gcd(s[2], s[3])
                        if g > 1:
                            g = gcd(s[0], gcd(s[1], g))
                            s = tuple(e/g for e in s)

                        if s in used: continue
                        #print s, g
                        #All larger similar triangles
                        h = 1
                        while h*s[3] <= limit:
                            hs = tuple(h*e for e in s)
                            if not (hs in used):

                                used[hs] = True
                                total += hs[3]
                            h += 1
    last = 0
    count = 1
    for e in sorted(used.keys(), key=itemgetter(3,0,1)):
        if e[3] == last:
            count += 1
            print e, factorize(e[3], ps, pa), count
        else:
            count = 1
            last = e[3]
            print e, factorize(e[3], ps, pa), count
    print 'v6', limit, total, len(T)



def solve7(limit):
    #Generate hypotenuse numbers up to limit
    phns, phma = generate_prime_hypotenuse_numbers(limit+1)
    total_r = 0
    reptuple = {}
    used = {}

    for i in xrange(1, 11): #5^10
        reptuple[(i,)] = int((i + 0.25)**2)
    for i in xrange(1, 7): #5 * 13 * 17 * 29 * 37* 41
        reptuple[(tuple([1]*i))] = (2*7**i - 3*3**i + 1)/6
    
    for p in phns:
        #Only one triangle is associated with a prime radius
        total_r += p
        used[p] = 1
        
        m = 2
        r = m*p
        while r <= limit:
            #Avoid double counting r = a*b = b*a
            if not (r in used):
                if phma[r]:
                    #counts = factor_hypotenuse_nums(r, phns)
                    n = r
                    counts = []
                    #factors = []
                    for f in phns:
                        if f > n: break
                        c = 0
                        while n % f == 0:
                            c += 1
                            #factors.append(f)
                            n //= f
                        if c > 0:
                            counts.append(c)
                    counts = tuple(sorted(counts))
                    #print r, counts, factors
                    if not (counts in reptuple):
                        reptuple[counts] = find_triangle(r)
                    used[r] = reptuple[counts]
                    total_r += (r * reptuple[counts])
                else:
                    used[r] = 1
                    total_r += r
            m += 1
            r = m*p
    #for e in sorted(used.keys()):
    #    print e, used[e]
    print "v7", limit, total_r
"""


