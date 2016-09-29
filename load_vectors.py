import numpy as np
from matrices import rot

#calculates the load vector from a load
def get_S_L( load, strut):
	dict = {
		1:{
			'1'  : S_L_1_1,
			'2a' : S_L_1_2a,
			'2b' : S_L_1_2b,
			'3'  : S_L_1_3
		},
		2:{
			'1'  : S_L_2_1,
			'2a' : S_L_2_2a,
			'2b' : S_L_2_2b,
			'3'  : S_L_2_3
		},
		3:{
			'1'  : S_L_3_1,
			'2a' : S_L_3_2a,
			'2b' : S_L_3_2b,
			'3'  : S_L_3_3
		}
	}

	x1 = load['x1']
	x2 = load['x2']
	l  = strut['l']
	F  = load['F']
	M  = load['M']
	q  = load['q']
	loadType = load['Type']
	strutType = strut['Type']

	return dict[loadType][strutType](x1, x2, l, F, M, q)

#adds up the load vectors and adds them to the strut dict
def assemble_S_L( strutLoads, struts, nodes ):
	#assemble strut IDs form dict
	StrutIDs = {}
	for ID, strut in struts.iteritems():
		StrutIDs[strut['ID']] = ID

	S_L = {}
	for ID, load in strutLoads.iteritems():
		strut = struts[StrutIDs[load['Strut']]]
		id = StrutIDs[strut['ID']]
		if id in S_L:
			S_L[id] += get_S_L(load, strut)
		else:
			S_L[id] = get_S_L(load, strut)

	for ID, v in S_L.iteritems():
		struts[ID]['S_L'] = v

	return struts

#creates the global load vector from strut loads and node loads
def assemble_S_G( nodeLoads, struts, nodes ):
	#assemble node IDs form dict
	NodeIDs = {}
	for ID, node in nodes.iteritems():
		NodeIDs[node['ID']] = ID

	size = len(nodes) * 3
	S_G = np.zeros(size)

	#add node loads
	for ID, load in nodeLoads.iteritems():
		id = NodeIDs[load['Node']]
		Fx = load['Fx']
		Fz = load['Fz']
		M  = load['M']
		v = np.array([Fx, Fz, M])
		for i in range(3):
			S_G[id*3 + i] += v[i]

	#change sign
	#sign = [-1, -1, -1, 1, 1, 1]
	#S_G = S_G * sign

	#add strut load vectors
	for ID, strut in struts.iteritems():
		id = NodeIDs[strut['StartNode']]

		S_L = np.zeros(6)
		if 'S_L' in strut:
			S_L = strut['S_L']

		#rotate to global coordinates
		alpha = strut['alpha']
		v = rot(alpha).dot(S_L)
		for i in range(6):
			S_G[id*3 + i] += v[i]

	return S_G

# Type 1
#  _______
# /       \______
# ---------------

def S_L_1_1( x1, x2, l, F, M, q ):
	a = x1/l
	b = x2/l

	A = ( ((1 - a)/2) + ((a**3 - b**3)/4) - ((a**4 - b**4)/10) ) * q * l
	B = (1 - ((a+b)/2)) * q * l - A

	fi = ( 1 - (1 - a + 0.3 * a**2) * 2 * a**2 - (1 - 0.6 * b) * b**3)
	Mi = fi * (q * l**2)/12

	fk = -1 * ( 1 - (1 - b + 0.3 * b**2) * 2 * b**2 - (1 - 0.6 * a) * a**3)
	Mk = fi * (q * l**2)/12

	S = np.array([0, A, Mi, 0, B, Mk])

	return S

def S_L_1_2a( x1, x2, l, F, M, q ):
	a = x1/l
	b = x2/l

	B = ((3/8) - (b/2) + ((b**2)/4) - ((a**3)/8) - ((b**4 - a**4)/40)) * q * l
	A = (1 - (b+a)/2) * q * l - B

	fi = 1 - ( (2/3) - (b**2)/5 ) * b**2 - ( (4/3) - a + (a**2)/5 ) * a**2
	Mi = fi * ((q * l**2)/8)

	S = np.array([0, A, Mi, 0, B, 0])

	return S

def S_L_1_2b( x1, x2, l, F, M, q ):
	a = x1/l
	b = x2/l

	A = ((3/8) - (a/2) + ((a**2)/4) - ((b**3)/8) - ((a**4 - b**4)/40)) * q * l
	B = (1 - (a+b)/2) * q * l - A

	fk = -1 * (1 - ( (2/3) - (a**2)/5 ) * a**2 - ( (4/3) - b + (b**2)/5 ) * b**2)
	Mk = fi * ((q * l**2)/8)

	S = np.array([0, A, 0, 0, B, Mk])

	return S

def S_L_1_3( x1, x2, l, F, M, q ):
	a = x1/l
	b = x2/l
	p = (a**2 - b**2)/3

	A = ((1 - a + p)/2) * q * l
	B = ((1 - b - p)/2) * q * l

	S = np.array([0, A, 0, 0, B, 0])

	return S


# Type 2
#     M+
# ---------------

def S_L_2_1( x1, x2, l, F, M, q ):
	a = x1/l
	b = (l-x1)/l

	A = -6 * a * b * (M/l)
	B = 6 * a * b * (M/l)

	Mi = (3 * b - 2) * b * M
	Mk = (3 * a - 2) * a * M

	S = np.array([0, A, Mi, 0, B, Mk])

	return S

def S_L_2_2a( x1, x2, l, F, M, q ):
	x2 = l - x1
	b = x2/l

	A = (1 - b**2) * 1.5 * (M/l)
	B = -1 * A

	Mi = ((3 * b**2 - 1)/2) * M

	S = np.array([0, A, Mi, 0, B, 0])

	return S

def S_L_2_2b( x1, x2, l, F, M, q ):
	a = x1/l

	A = -1 * (1 - a**2) * 1.5 * (M/l)
	B = -1 * A

	Mk = ((3 * a**2 - 1)/2) * M

	S = np.array([0, A, 0, 0, B, Mk])

	return S

def S_L_2_3( x1, x2, l, F, M, q ):
	A = -1 * (M/l)
	B = (M/l)

	S = np.array([0, A, 0, 0, B, 0])

	return S

# Type 3
#      F+
# ---------------

def S_L_3_1( x1, x2, l, F, M, q ):
	a = x1/l
	b = (l-x1)/l

	A = (3 - 2 * b) * b**2 * F
	B = (3 - 2 * a) * a**2 * F

	Mi = a * b**2 * F * l
	Mk = -1 * a**2 * b * F * l

	S = np.array([0, A, Mi, 0, B, Mk])

	return S

def S_L_3_2a( x1, x2, l, F, M, q ):
	a = x1/l
	b = (l-x1)/l

	A = ((3 - b**2)/2) * b * F
	B = ((3 - a)/2) * a**2 * F

	Mi = ((1 - b**2)/2) * a * F * l

	S = np.array([0, A, Mi, 0, B, 0])

	return S

def S_L_3_2b( x1, x2, l, F, M, q ):
	a = x1/l
	b = (l-x1)/l

	A = ((3 - b)/2) * b**2 * F
	B = ((3 - a**2)/2) * a * F

	Mk = -1 * ((1 - a**2)/2) * a * F * l

	S = np.array([0, A, 0, 0, B, Mk])

	return S

def S_L_3_3( x1, x2, l, F, M, q ):
	a = x1/l
	b = (l-x1)/l

	A = b * F
	B = a * F

	S = np.array([0, A, 0, 0, B, 0])

	return S
