import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
from util import *

def midPoint( (x1, y1), (x2, y2) ):
	x = x1 + (x2 - x1)/2
	y = y1 + (y2 - y1)/2
	return (x, y)

def normalize(v):
	norm = np.linalg.norm(v)
	if norm == 0: 
		return v
	return v/norm

def rotate(v,theta):
	c = np.cos(theta);
	s = np.sin(theta);
	return (c*v[0] - s*v[1], s*v[0]+ c*v[1])

def drawBeam( start, end, id, size, ax ):
	width = size

	x1 = start[0]
	y1 = start[1]
	x2 = end[0]
	y2 = end[1]

	beam = plt.plot([x1, x2], [y1, y2], '-', color="black", lw=width)

	v = np.array([x2-x1,y2-y1])
	v = normalize(v)
	v = v * size/4
	v = rotate(v, np.pi*-0.5)

	x1 = x1 + v[0]
	y1 = y1 + v[1]
	x2 = x2 + v[0]
	y2 = y2 + v[1]

	fibre = plt.plot([x1, x2], [y1, y2], '--', color="black")

	mid = midPoint((x1,y1),(x2,y2))
	x = mid[0] + v[0] * 5
	y = mid[1] + v[1] * 5
	ax.text(x, y, id, bbox=dict(boxstyle='round,pad=0.3', ec='black', fc='w'))

	return [beam, fibre]

def drawNode( point, size, color, ax ):
	size = float(size)/10

	node = plt.Circle(point, size, color=color, clip_on=False)
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

def bezier(verts, size, ax):
	width = size

	codes = [Path.MOVETO,
					 Path.CURVE4,
					 Path.CURVE4,
					 Path.CURVE4,
					]

	path = Path(verts, codes)
 
	patch = patches.PathPatch(path, edgecolor='yellow', facecolor='none', lw=width)
	ax.add_patch(patch)

	#debug
	#xs, ys = zip(*verts)
	#ax.plot(xs, ys, 'x--', lw=2, color='red', ms=10)

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

def drawNodes(nodes, size, ax):
	for ID, node in nodes.iteritems():
		_x = node['X']
		_z = node['Z']
		id = node['ID']

		drawNode((_x,_z), size, 'black', ax)
		ax.text(_x - size, _z - size, id, bbox=dict(boxstyle='round,pad=0.2',
																											ec='white',
																											fc='white'))

def drawConstraints(constraints, nodes, mid, size, ax):
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

def drawStruts(struts, nodes, size, ax):
	for ID, strut in struts.iteritems():
		node = nodeNameToID(strut['StartNode'], nodes)
		_x1 = nodes[node]['X']
		_z1 = nodes[node]['Z']

		node = nodeNameToID(strut['EndNode'], nodes)
		_x2 = nodes[node]['X']
		_z2 = nodes[node]['Z']

		drawBeam((_x1,_z1), (_x2,_z2), nodes[node]['ID'], size, ax)

def drawDisplacedNodes(d, nodes, size, ax):
	_d = [d[n:n+3] for n in range(0, len(d), 3)]

	i = 0
	for ID, node in nodes.iteritems():
		_x = node['X'] + _d[i][0]
		_z = node['Z'] + _d[i][1]
		node['Xd'] = _x
		node['Zd'] = _z
		node['rd'] = _d[i][2]
		i += 1
		drawNode((_x,_z), size, 'yellow', ax)

def drawDisplacedStruts(struts, nodes, size, ax):
	for ID, strut in struts.iteritems():
		node = nodeNameToID(strut['StartNode'], nodes)
		_x1d = nodes[node]['Xd']
		_x1  = nodes[node]['X']
		_z1d = nodes[node]['Zd']
		_z1  = nodes[node]['Z']
		_rd1 = nodes[node]['rd']

		node = nodeNameToID(strut['EndNode'], nodes)
		_x2d = nodes[node]['Xd']
		_x2  = nodes[node]['X']
		_z2d = nodes[node]['Zd']
		_z2  = nodes[node]['Z']
		_rd2 = nodes[node]['rd']

		mid = midPoint( (_x1, _z1), (_x2, _z2) )
		v = [_x2 - mid[0], _z2 - mid[1]]
		v = rotate(v,_rd1)
		vert2 = (_x1d + v[0], _z1d + v[1])

		mid = midPoint((_x1, _z1), (_x2, _z2) )
		v = [(_x2 - mid[0]) * -1, (_z2 - mid[1]) * -1]
		v = rotate(v,_rd2)
		vert3 = (_x2d + v[0], _z2d + v[1])

		verts = [ (_x1d, _z1d),
							vert2,
							vert3,
							(_x2d, _z2d)]

		bezier(verts, size, ax)

def getPlotLimit(ax):
	lim_x = ax.get_xlim()
	lim_y = ax.get_ylim()

	if abs(lim_x[1]) > abs(lim_y[1]):
		return lim_x
	else:
		return lim_y

def drawSystem(nodes, struts, constraints, d, size, savePlot):
	_min, _max, mid = getBounds(nodes)
	fig, ax = plt.subplots() 

	#plt.xlabel('x label')
	#plt.ylabel('y label')

	# Nodes
	drawNodes(nodes, size, ax)

	# Constraints
	drawConstraints(constraints, nodes, mid, size, ax)

	# Struts
	drawStruts(struts, nodes, size, ax)
	
	##############################################################################

	# Displaced nodes
	drawDisplacedNodes(d, nodes, size, ax)

	# Displaced struts
	drawDisplacedStruts(struts, nodes, size, ax)

	##############################################################################

	lim = getPlotLimit(ax)
	offset = abs(lim[1]/10)
	x1,x2,y1,y2 = plt.axis()
	plt.axis((x1-offset,x2+offset,y1-offset,y2+offset))
	plt.title("System")
	ax.set_aspect('equal')

	if savePlot != False:
		plt.savefig(savePlot, bbox_inches='tight')
	else:
		plt.show()