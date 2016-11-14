import scipy.linalg as sp
from util import *

def solver(K, S_G, constraints, nodes):
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