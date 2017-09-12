import scipy.linalg as sp
from util import *
from matrices import calc_local_forces, calculateKgeom

def calculateN(nodes, struts, d):
	calc_local_forces(nodes, struts, d)

	for ID, strut in struts.iteritems():
		strut["N"] = strut["Sl"][0]


def solveLinear(K, S_G, constraints, nodes):
	d = sp.solve(K,S_G)

	#apply constraints: set d[i] = 0
	for ID, const in constraints.iteritems():
		id = nodeNameToID(const['Node'], nodes)
		if const['x']:
			x = id * 3
			d[x] = 0
		if const['z']:
			x = id * 3 + 1
			d[x] = 0
		if const['r']:
			x = id * 3 + 2
			d[x] = 0

	return d


def solver(K, S_G, constraints, nodes, struts, epsilon, secondOrder):
	d = solveLinear(K, S_G, constraints, nodes)

	if secondOrder:
		#first iteration with N=0
		for ID, strut in struts.iteritems():
			strut["N"] = 0
		#iteration
		i = 1
		while True:
			#save the last result
			lastN = {}
			for ID, strut in struts.iteritems():
				lastN[ID] = strut["N"]

			#calculate new result
			calculateN(nodes, struts, d)

			Kgeom = calculateKgeom(struts, nodes)
			d = solveLinear(K+Kgeom, S_G, constraints, nodes)

			#calculate largest delta
			newN = {}
			for ID, strut in struts.iteritems():
				newN[ID] = strut["N"]

			delta = []
			for ID, N in lastN.iteritems():
				delta.append(abs(N - newN[ID]))

			delta = max(delta)

			print "Iteration " + str(i) + ": delta = " + str(delta)
			i += 1

			if delta <= epsilon:
				print "\n"
				break

	return d