import pygame
import numpy as np

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)

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

	return _min, _max

def normalize(v):
	norm = np.linalg.norm(v)
	if norm == 0: 
		return v
	return v/norm

def rotate(v,theta):
	c = np.cos(theta);
	s = np.sin(theta);
	return (c*v[0] - s*v[1], s*v[0]+ c*v[1])

def drawSupport_2(screen,x,y,size):
	triangle = [(x,y), (x+size/2,y+size), (x-size/2,y+size), (x,y)]

	pygame.draw.lines(screen, white, False, triangle, 2)
	pygame.draw.circle(screen, white, (x,y), size/3, 0)

def drawSupport_1(screen,x,y,size):
	triangle = [(x,y), (x+size/2,y+size), (x-size/2,y+size), (x,y)]
	line = [(x+size/2,y+size*1.1+2), (x-size/2,y+size*1.1+2)]

	pygame.draw.lines(screen, white, False, triangle, 2)
	pygame.draw.lines(screen, white, False, line, 2)
	pygame.draw.circle(screen, white, (x,y), size/3, 0)

def drawSupport_3(screen,x,y,size):
	line = [(x,y+size/2), (x,y-size/2)]
	diagonals = [[(x,y-size/2),(x-size/3,y-size/6)],
							 [(x,y-size/6),(x-size/3,y+size/6)],
							 [(x,y+size/6),(x-size/3,y+size/2)]]

	pygame.draw.lines(screen, white, False, line, 2)
	for lines in diagonals:
		pygame.draw.lines(screen, white, False, lines, 2)

def drawNode(screen,x,y,size):
	pygame.draw.circle(screen, white, (int(x),int(y)), int(size/10), 0)

def drawStrut(screen, start, end, size):
	x1 = start[0]
	y1 = start[1]
	x2 = end[0]
	y2 = end[1]

	line = [start,end]
	pygame.draw.lines(screen, white, False, line, 2)

	v = np.array([x2-x1,y2-y1])
	v = normalize(v)
	v = v * size/4
	v = rotate(v, np.pi*3/4)

	start = (x1 + v[0], y1 + v[1])
	end   = (x2 + v[0], y2 + v[1])

	#draw_dashed_line(screen, start, end, size)

def renderSystem(nodes, struts, constraints, size):
	offsetZ = 100
	offsetX = 100

	#assemble node IDs form dict
	NodeIDs = {}
	for ID, node in nodes.iteritems():
		NodeIDs[node['ID']] = ID

	screen = pygame.display.set_mode((640,480))
	
	for ID, node in nodes.iteritems():
		_x = node['X']
		_z = node['Z']
		_x += offsetX
		_z += offsetZ

		drawNode( screen, _x, _z, size)

	for ID, const in constraints.iteritems():
		_x = nodes[NodeIDs[const['Node']]]['X']
		_z = nodes[NodeIDs[const['Node']]]['Z']
		_x += offsetX
		_z += offsetZ

		x = const['x']
		z = const['z']
		r = const['r']

		#if x and z and r:
		drawSupport_3( screen, _x, _z, size )

	for ID, strut in struts.iteritems():
		_x1 = nodes[NodeIDs[strut['StartNode']]]['X']
		_z1 = nodes[NodeIDs[strut['StartNode']]]['Z']
		_x1 += offsetX
		_z1 += offsetZ

		_x2 = nodes[NodeIDs[strut['EndNode']]]['X']
		_z2 = nodes[NodeIDs[strut['EndNode']]]['Z']
		_x2 += offsetX
		_z2 += offsetZ

		drawStrut(screen, (_x1,_z1), (_x2,_z2), size)

	while 1:
		pygame.display.update()