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

def drawSupport_3(x,y,size):
	width = size
	size = float(size)/2

	line_x = [x, x]
	line_y = [y-size, y+size]
	
	diagonals = [[[x,x+size/1.5],[y+size,y+size/3]],
							 [[x,x+size/1.5],[y+size/3,y-size/3]],
							 [[x,x+size/1.5],[y-size/3,y-size]]]

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

def drawSupport_1(x,y,size,ax):
	width = size
	size = float(size)/2
	
	triangle_x = [x, x+size, x-size, x]
	triangle_y = [y, y-size, y-size, y]

	line_x = [x+size, x-size]
	line_y = [y-size*1.3, y-size*1.3]

	plt.plot(triangle_x, triangle_y, '-', color="blue", lw=width)
	plt.plot(line_x, line_y, '-', color="blue", lw=width)
	circle = plt.Circle((x,y), size/5, color="blue", clip_on=False)
	ax.add_artist(circle)

def drawSystem(nodes, struts, constraints, size):

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

		#if x and z and r:
		drawSupport_3(_x, _z, size)

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
	lim 				= ax.get_xlim()
	offset			= abs(lim[1]/10)
	plt.axis((x1-offset,x2+offset,y1-offset,y2+offset))

	plt.show()