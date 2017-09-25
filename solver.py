import scipy.linalg as sp
from util import *
from matrices import *

def calculateN(nodes, struts, d):
	calc_local_forces(nodes, struts, d)

	for ID, strut in struts.iteritems():
		Ni = strut['Sl'][0]
		Nk = strut['Sl'][3]
		if Ni == 0:
			strut['N'] = Nk
		elif Nk == 0:
			strut['N'] = Ni
		else:
			strut['N'] = Nk


def solveLinear(K, S_G, constraints, nodes):
	
	if sp.det(K) == 0:
		print('System is kinematic (det(K)=0)!')
		exit()
		
	d = sp.solve(K, S_G)

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


def solver(S_G, constraints, nodes, struts, epsilon, secondOrder, debug, interBound):

	#first iteration with N=0
	for ID, strut in struts.iteritems():
		strut["N"] = 0

	K = assemble_global_K_I(nodes, struts)
	apply_constraints(K, struts, nodes, constraints)
	K = symmetrize(K)

	# update strut K
	applyConstToStrutK(struts, constraints)

	d = solveLinear(K, S_G, constraints, nodes)

	printDebugMatrix("K", K, debug)

	if secondOrder:

		calculateN(nodes, struts, d)

		#iteration
		i = 1
		print "################################################################################"
		
		while True:
			#save the last result
			lastN = {}
			for ID, strut in struts.iteritems():
				lastN[ID] = strut["N"]

			K = assemble_global_K_I(nodes, struts)
			Kgeom = calculateKgeom(struts, nodes)

			printDebugMatrix("K", K, debug)

			K += Kgeom

			apply_constraints(K, struts, nodes, constraints)
			K = symmetrize(K)

			d = solveLinear(K, S_G, constraints, nodes)

			# update strut K
			for ID, strut in struts.iteritems():
				N = strut["N"]
				l = strut["l"]

				strut['K'] += Kgeom_(N,l)

			applyConstToStrutK(struts, constraints)

			#calculate new result
			calculateN(nodes, struts, d)

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
				# debug
				printDebugMatrix("K + Kgeom", K, debug)
				printDebugMatrix("Kgeom", Kgeom, debug)
				
				print "################################################################################"
				print ""
	
				break

			if i >= interBound:
				print('System is unstable (delta N not converging after ' + str(i) + ' iterations)!')
				exit()

	return d