import matplotlib.pyplot as plt
import numpy as np
from util import *

def normalize(v):
	norm = np.linalg.norm(v)
	if norm == 0: 
		return v
	return v/norm

def rotate(v,theta):
	c = np.cos(theta);
	s = np.sin(theta);
	return (c*v[0] - s*v[1], s*v[0]+ c*v[1])

def drawBeam( start, end, size ):
	width = size

	x1 = start[0]
	y1 = start[1]
	x2 = end[0]
	y2 = end[1]

	beam = plt.plot([x1, x2], [y1, y2], '-', color="black", lw=width)

	v = np.array([x2-x1,y2-y1])
	v = normalize(v)
	v = v * size/4
	v = rotate(v, np.pi*-1/2)

	x1 = x1 + v[0]
	y1 = y1 + v[1]
	x2 = x2 + v[0]
	y2 = y2 + v[1]

	fibre = plt.plot([x1, x2], [y1, y2], '--', color="black")

	return [beam, fibre]

def drawNode( point, size, ax ):
	size = float(size)/10

	node = plt.Circle(point, size, color='black', clip_on=False)
	ax.add_artist(node)

def drawSupport_3(x,y,orientation,size):
	width = size
	size = float(size)/2

	line_x = [x, x]
	line_y = [y-size, y+size]

	if orientation == 'r':
		diagonals = [[[x,x+size/1.5],[y+size,y+size/3]],
								 [[x,x+size/1.5],[y+size/3,y-size/3]],
								 [[x,x+size/1.5],[y-size/3,y-size]]]
	
	else:
		diagonals = [[[x,x-size/1.5],[y+size,y+size/3]],
								 [[x,x-size/1.5],[y+size/3,y-size/3]],
								 [[x,x-size/1.5],[y-size/3,y-size]]]

	plt.plot(line_x, line_y, '-', color="blue", lw=width )
	for lines in diagonals:
		plt.plot(lines[0], lines[1], '-', color="blue", lw=width)

def drawSupport_2(x,y,size,ax):
	width = size
	size = float(size)/2
	triangle_x = [x, x+size, x-size, x]
	triangle_y = [y, y-size, y-size, y]

	plt.plot(triangle_x, triangle_y, '-', color="blue", lw=width)
	circle = plt.Circle((x,y), size/5, color="blue", clip_on=False)
	ax.add_artist(circle)

def drawSupport_1_z(x,y,size,ax):
	width = size
	size = float(size)/2
	
	triangle_x = [x, x+size, x-size, x]
	triangle_y = [y, y-size, y-size, y]

	line_x = [x+size, x-size]
	line_y = [y-size*1.3, y-size*1.3]
	line_y = [y-size*1.3, y-size*1.3]

	plt.plot(triangle_x, triangle_y, '-', color="blue", lw=width)
	plt.plot(line_x, line_y, '-', color="blue", lw=width)
	circle = plt.Circle((x,y), size/5, color="blue", clip_on=False)
	ax.add_artist(circle)

def drawSupport_1_x(x,y,orientation,size,ax):
	width = size
	size = float(size)/2

	if orientation == 'r':
		triangle_x = [x, x+size, x+size, x]
		triangle_y = [y, y+size, y-size, y]

		line_x = [x+size*1.3, x+size*1.3]
		line_y = [y+size, y-size]

	else:
		triangle_x = [x, x-size, x-size, x]
		triangle_y = [y, y+size, y-size, y]

		line_x = [x-size*1.3, x-size*1.3]
		line_y = [y+size, y-size]

	plt.plot(triangle_x, triangle_y, '-', color="blue", lw=width)
	plt.plot(line_x, line_y, '-', color="blue", lw=width)
	circle = plt.Circle((x,y), size/5, color="blue", clip_on=False)
	ax.add_artist(circle)

def drawSupport_4(x,y,size,ax):
	size = float(size)/2

	circle = plt.Circle((x,y), size, color="blue", fill=False, clip_on=False)
	ax.add_artist(circle)

def getBounds(nodes):
	_min = [0,0]
	_max = [0,0]

	for ID, node in nodes.iteritems():
		#max
		if node['X'] > _max[0]:
			_max[0] = node['X']
		if node['Z'] > _max[1]:
			_max[1] = node['Z']
		#min
		if node['X'] < _min[0]:
			_min[0] = node['X']
		if node['Z'] < _min[1]:
			_min[1] = node['Z']

	if _min[0] < 0:
		__min = abs(_min[0])
		mid = (__min + _max[0])/2
	else:
		mid = (_max[0] - _min[0])/2

	return _min, _max, mid

def drawSystem(nodes, struts, constraints, size):

	_min, _max, mid = getBounds(nodes)

	fig, ax = plt.subplots() 

	#plt.xlabel('x label')
	#plt.ylabel('y label')

	for ID, node in nodes.iteritems():
		_x = node['X']
		_z = node['Z']

		drawNode((_x,_z), size, ax)

	for ID, const in constraints.iteritems():
		node = nodeNameToID(const['Node'], nodes)
		_x = nodes[node]['X']

		node = nodeNameToID(const['Node'], nodes)
		_z = nodes[node]['Z']

		x = const['x']
		z = const['z']
		r = const['r']

		if _x < mid:
			orientation = 'l'
		else:
			orientation = 'r'
		
		if x and z and r:
			drawSupport_3(_x, _z, orientation, size)
		elif x and z:
			drawSupport_2(_x, _z, size, ax)
		elif x and r:
			drawSupport_1_x(_x, _z, orientation, size, ax)
			drawSupport_4(_x,_z,size,ax)
		elif z and r:
			drawSupport_1_z(_x, _z, size, ax)
			drawSupport_4(_x,_z,size,ax)
		elif z:
			drawSupport_1_z(_x, _z, size, ax)
		elif x:
			drawSupport_1_x(_x, _z, orientation, size, ax)
		elif r:
			drawSupport_4(_x,_z,size,ax)

	for ID, strut in struts.iteritems():
		node = nodeNameToID(strut['StartNode'], nodes)
		_x1 = nodes[node]['X']
		_z1 = nodes[node]['Z']

		node = nodeNameToID(strut['EndNode'], nodes)
		_x2 = nodes[node]['X']
		_z2 = nodes[node]['Z']

		drawBeam((_x1,_z1), (_x2,_z2), size)
	

	plt.title("System")
	ax.set_aspect('equal')
	
	x1,x2,y1,y2 = plt.axis()
	lim_x				= ax.get_xlim()
	lim_y				= ax.get_ylim()

	if abs(lim_x[1]) > abs(lim_y[1]):
		lim = lim_x
	else:
		lim = lim_y

	offset			= abs(lim[1]/10)
	plt.axis((x1-offset,x2+offset,y1-offset,y2+offset))

	plt.show()