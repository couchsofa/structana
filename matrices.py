import math
import numpy as np
from util import *

def _e( E, I, l, N ):
	e = l*math.sqrt(float(abs(N))/float(E*I))
	if e >= np.pi * 2:
		print('System is unstable (e = ' + str(e) + ' >= 2*pi)!')
		exit()
	return e

def _A( e, N ):
	if e <= 0:
		return 4
	# negative normal pressure
	if N < 0:
		if e >= 1.431 * np.pi:
			print 'System is unstable (Euler III e >= 1,431*pi)!'
			exit()
		return (e * math.sin(e) - e**2 * math.cos(e))\
						/(2 * (1 - math.cos(e)) - (e * math.sin(e)))
	# positive normal pressure
	else:
		return ( e * math.sinh( e ) - e**2 * math.cosh( e ) )\
						/(2 * ( 1- math.cosh(e)) + e * math.sinh(e))

def _B( e, N ):
	if e <= 0:
		return 2
	# negative normal pressure
	if N < 0:
		return (e**2 - e * math.sin(e) )\
						/( 2*(1 - math.cos(e)) - e * math.sin(e) )
	# positive normal pressure
	else:
		return (e**2 - e * math.sinh(e))\
						/(2*(1 - math.cosh(e)) + e * math.sinh(e))

def _C( e, N ):
	if e <= 0:
		return 3
	# negative normal pressure
	if N < 0:
		if e >= np.pi:
			print 'System is unstable (Euler II e >= pi)!'
			exit()
		return (e**2 * math.sin(e))\
						/(math.sin(e) - e * math.cos(e))
	# positive normal pressure
	else:
		return (e**2 * math.sinh(e))\
						/( math.sinh(e) - e * math.cosh(e))


def _D( e, N ):
	if N < 0 and e > np.pi:
		return 0
	return _A(e, N) + _B(e, N)

#rotation matrix for angle alpha
def rot(alpha):
	if alpha == 360.0:
		alpha = 0
	alpha = np.deg2rad(alpha)
	r = np.array([[math.cos(alpha)		, math.sin(alpha)	, 0	, 0									, 0								, 0	],
							  [-1*math.sin(alpha)	, math.cos(alpha)	, 0	, 0									, 0								, 0	],
							  [0									, 0								, 1	, 0									, 0								, 0	],
							  [0									, 0								, 0	, math.cos(alpha)		, math.sin(alpha)	, 0	],
							  [0									, 0								, 0	, -1*math.sin(alpha), math.cos(alpha)	, 0	],
							  [0									, 0								, 0	, 0									, 0								, 1	]])

	return r


# apply the constraints to K saved in struts
def applyConstToStrutK(struts, constraints):
	for ID, strut in struts.iteritems():
		zero = np.zeros(6)

		node = strut['StartNode']
		id = 0
		const = getConsttraint(node, constraints)

		if const:
			if const['x']:
				x = id * 3
				strut["K"][:,x] = zero
				strut["K"][x,:] = zero
			if const['z']:
				x = id * 3 + 1
				strut["K"][:,x] = zero
				strut["K"][x,:] = zero
			if const['r']:
				x = id * 3 + 2
				strut["K"][:,x] = zero
				strut["K"][x,:] = zero

		node = strut['EndNode']
		id = 1
		const = getConsttraint(node, constraints)

		if const:
			if const['x']:
				x = id * 3
				strut["K"][:,x] = zero
				strut["K"][x,:] = zero
			if const['z']:
				x = id * 3 + 1
				strut["K"][:,x] = zero
				strut["K"][x,:] = zero
			if const['r']:
				x = id * 3 + 2
				strut["K"][:,x] = zero
				strut["K"][x,:] = zero

		#check for zeros in column and row
		for i in range(6):
			if np.all(strut["K"][:,i] == 0) and np.all(strut["K"][i,:] == 0):
				strut["K"][i][i] = 1


#create strut matrix
def create_strut_K(strut):
	alpha = strut['alpha']
	l = strut['l']
	E = strut['E']
	A = strut['A']
	I = strut['I']
	Type = strut['Type']
	N = strut['N']

	if Type == '3':
		K = K_3_I(E, A, l)
	elif Type == '2a':
		K = K_2a_I( E, I, A, l, N )
	elif Type == '2b':
		K = K_2b_I( E, I, A, l, N )
	elif Type == '1':
		K = K_1_I( E, I, A, l, N )

	r = rot(alpha)
	K = np.dot(r, K)

	strut["K"] = K

	return K

#assemble the global stiffness matrix
def assemble_global_K_I(nodes, struts):
	global_K = create_global_K(nodes)

	for ID, strut in struts.iteritems():
		
		K = create_strut_K(strut)

		insertion_point = nodeNameToID(strut['StartNode'], nodes) * 3
		global_K = insert( global_K, K, insertion_point, insertion_point, lambda x,y: x+y )

	return global_K

def apply_constraints(K, struts, nodes, constraints):
	#apply constraints
	size = len(nodes) * 3
	zero = np.zeros(size)
	for ID, const in constraints.iteritems():
		id = nodeNameToID(const['Node'], nodes)
		if const['x']:
			x = id * 3
			K[:,x] = zero
			K[x,:] = zero
		if const['z']:
			x = id * 3 + 1
			K[:,x] = zero
			K[x,:] = zero
		if const['r']:
			x = id * 3 + 2
			K[:,x] = zero
			K[x,:] = zero

	#check for zeros in column and row
	for i in range(len(K[0])):
		if np.all(K[:,i] == 0) and np.all(K[i,:] == 0):
			K[i][i] = 1

# |-------|
def K_1_I( E, I, A, l, N ):
	e = _e( E, I, l, N )
	a = _A( e, N )
	b = _B( e, N )
	c = _C( e, N )
	d = _D( e, N )

	EI = E*I
	EA = E*A

	K = np.array([[(EA)/l	, 0								, 0							, -1*(EA)/l	, 0								, 0								],
							  [0			, 2*d*((EI)/l**3)	, -1*d*(EI/l**2), 0					, -2*d*(EI/l**3)	, -1*d*(EI/l**2)	],
							  [0			, 0								, a*(EI/l)			, 0					, d*(EI/l**2)			, b*(EI/l)				],
							  [0			, 0								, 0							, EA/l			, 0								, 0								],
							  [0			, 0								, 0							, 0					, 2*d*(EI/l**3)		, d*(EI/l**2)			],
							  [0			, 0								, 0							, 0					, 0								, a*(EI/l)				]])

	return K

# |------o|
def K_2a_I( E, I, A, l, N ):
	e = _e( E, I, l, N )
	a = _A( e, N )
	b = _B( e, N )
	c = _C( e, N )
	d = _D( e, N )

	EI = E*I
	EA = E*A

	K = np.array([[EA/l	, 0					, 0							, -1*(EA)/l	, 0							, 0],
							  [0		, c*(EI/l)	, -1*c*(EI/l**2), 0					, -1*(EI/l**3)	, 0],
							  [0		, 0					, c*(EI/l)			, 0					, c*(EI/l**2)		, 0],
							  [0		, 0					, 0							, EA/l			, 0							, 0],
							  [0		, 0					, 0							, 0					, c*(EI/l**3)		, 0],
							  [0		, 0					, 0							, 0					, 0							, 0]])

	return K

# |o------|
def K_2b_I( E, I, A, l, N ):
	e = _e( E, I, l, N )
	a = _A( e, N )
	b = _B( e, N )
	c = _C( e, N )
	d = _D( e, N )

	EI = E*I
	EA = E*A

	K = np.array([[EA/l	, 0				, 0	,-1*(EA/l)	, 0								, 0							],
							  [0		, EI/l**3	, 0	,0					, -1*c*(EI/l**3)	, -1*c*(EI/l**2)],
							  [0		, 0				, 0	,0					, 0								, 0							],
							  [0		, 0				, 0	,EA/l				, 0								, 0							],
							  [0		, 0				, 0	,0					, c*(EI/l**3)			, c*(EI/l**2)		],
							  [0		, 0				, 0	,0					, 0								, c*(EI/l)			]])

	return K

# |o-----o|
def K_3_I( E, A, l ):

	EA = E*A

	K = np.array([[EA/l	, 0	, 0	, -1*(EA)/l	, 0	, 0],
							  [0		, 0	, 0	, 0					, 0	, 0],
							  [0		, 0	, 0	, 0					, 0	, 0],
							  [0		, 0	, 0	, EA/l			, 0	, 0],
							  [0		, 0	, 0	, 0					, 0	, 0],
							  [0		, 0	, 0	, 0					, 0	, 0]])

	return K

def Kgeom_(N, l):
	if N <= 0:
		K = np.array([[0, 0			 , 0, 0, 0,			  0],
					  [0, -1*abs(N)/l, 0, 0, abs(N)/l,	  0],
					  [0, 0			 , 0, 0, 0, 		  0],
					  [0, 0			 , 0, 0, 0,			  0],
					  [0, 0			 , 0, 0, -1*abs(N)/l, 0],
					  [0, 0			 , 0, 0, 0,			  0]])
	else:
		K = np.array([[0, 0			 , 0, 0, 0,			  0],
					  [0, abs(N)/l   , 0, 0, -1*abs(N)/l, 0],
					  [0, 0			 , 0, 0, 0, 		  0],
					  [0, 0			 , 0, 0, 0,			  0],
					  [0, 0			 , 0, 0, abs(N)/l,    0],
					  [0, 0			 , 0, 0, 0,			  0]])

	return K

def calculateKgeom(struts, nodes):
	size = len(nodes) * 3
	K = np.zeros( (size, size) )

	for ID, strut in struts.iteritems():
		N = strut["N"]
		l = strut["l"]
		
		Kgeom = Kgeom_(N,l)

		insertion_point = nodeNameToID(strut['StartNode'], nodes) * 3
		K = insert( K, Kgeom, insertion_point, insertion_point, lambda x,y: x+y )

	return K


def symmetrize(M):
	return M + M.T - np.diag(M.diagonal())

def create_global_K( nodes ):
	size = len(nodes) * 3
	K = np.zeros( (size, size) )
	return K

# Insert overlapping matrices 
# Ignores values below the diagonal
def insert( M, K, start_x, start_y, fn ):
	size_x, size_y = K.shape

	if (start_x + size_x > M.shape[0]) or (start_y + size_y > M.shape[1]):
		print "Size mismatch inserting K into M at (" + str(start_x) + "," + str(start_y) + ")."
		exit()

	for y in range(size_y):
		for x in range(size_x - y):
			M[start_y + y][start_x + x + y] = fn(M[start_y + y][start_x + x + y], K[y][x + y])
	return M

def countConst( constraints ):
	n = 0
	for ID, const in constraints.iteritems():
		n += const['x'] + const['z'] + const['r']

	return n

# calculate the local strut forces
def calc_local_forces(nodes, struts, d):
	for ID, strut in struts.iteritems():
		alpha = strut['alpha']
		K = strut["K"]
		r = rot(alpha)

		x1 = nodeNameToID(strut["StartNode"], nodes) * 3
		x2 = x1 + 3
		x3 = nodeNameToID(strut["EndNode"], nodes) * 3
		x4 = x3 + 3

		dl = np.append(d[x1:x2], d[x3:x4]*-1)

		Sg = np.dot(K, dl)
		Sl = np.dot(r, Sg)

		strut["Sl"] = Sl

