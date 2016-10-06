import csv
from input_templates import *
import numpy as np

def typeConv(_dict, _typeTemplate):
	_typeTemplate = dict(_typeTemplate)
	for key, value in _dict.iteritems():
		try:
			_dict[key] = _typeTemplate[key](value)
		except ValueError:
			print('The ' + key + ' value is not of type ' + str(_typeTemplate[key]) + '.')
			exit()

	return _dict

def readCSV(csvFile, typeTemplate):
	ID = 0
	with open(csvFile) as csvfile:
		_dict = {}
		reader = csv.DictReader(csvfile, delimiter = ';')

		for row in reader:
			row = typeConv(row, typeTemplate)
			_dict[ID] = row
			ID += 1

	return _dict

def genTemplate(filename, typeTemplate):
	fieldnames = []
	for key, value in typeTemplate:
		fieldnames.append(key)
	with open(filename + '.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter = ';')
		writer.writerow(fieldnames)

def checkStrutNodes(nodes, struts):
	#assemble node IDs form dict
	NodeIDs = []
	for ID, node in nodes.iteritems():
		NodeIDs.append(node['ID'])

	for ID, strut in struts.iteritems():
		if strut['StartNode'] not in NodeIDs:
			print('Node ' + str(strut['StartNode']) + ' referenced by strut ' + str(strut['ID']) + ' but not defined.')
			exit()
		if strut['EndNode'] not in NodeIDs:
			print('Node ' + str(strut['EndNode']) + ' referenced by strut ' + str(strut['ID']) + ' but not defined.')
			exit()

def checkConstraintNodes(nodes, constraints):
	#assemble node IDs form dict
	NodeIDs = []
	for ID, node in nodes.iteritems():
		NodeIDs.append(node['ID'])

	for ID, const in constraints.iteritems():
		if const['Node'] not in NodeIDs:
			print('Node ' + str(const['Node']) + ' referenced by constraint ' + str(ID) + ' but not defined.')
			exit()

def checkStrutLoads(struts, strutLoads):
	#assemble strut IDs form dict
	StrutIDs = []
	for ID, strut in struts.iteritems():
		StrutIDs.append(strut['ID'])

	for ID, load in strutLoads.iteritems():
		if load['Strut'] not in StrutIDs:
			print('Strut ' + str(load['Strut']) + ' referenced by load ' + str(ID) + ' but not defined.')
			exit()

def checkNodeLoads(nodes, nodeLoads):
	#assemble node IDs form dict
	NodeIDs = []
	for ID, node in nodes.iteritems():
		NodeIDs.append(node['ID'])

	for ID, load in nodeLoads.iteritems():
		if load['Node'] not in NodeIDs:
			print('Node ' + str(load['Node']) + ' referenced by load ' + str(ID) + ' but not defined.')
			exit()

def deleteFreeNodes(nodes, struts):
	#assemble node IDs form dict
	NodeIDs = {}
	for ID, node in nodes.iteritems():
		NodeIDs[ID] = node['ID']

	freeNodes = []
	for ID, node in nodes.iteritems():
		isFreeNode = True
		for strutID, strut in struts.iteritems():
			if (strut['StartNode'] == NodeIDs[ID]) or (strut['EndNode'] == NodeIDs[ID]):
				isFreeNode = False
				pass
		if isFreeNode:
			print('Node ' + str(NodeIDs[ID]) + ' is a free node and will be deleted.')
			freeNodes.append(ID)

	for freeNode in freeNodes:
		del nodes[freeNode]

	#return nodes

def getStrutLength(nodes, struts):
	for ID, strut in struts.iteritems():
		strut['l'] = strutLength(strut, nodes)

def getStrutAngle(nodes, struts):
	for ID, strut in struts.iteritems():
		strut['alpha'] = strutAngle(strut, nodes)

def getStrutType(struts):
	for ID, strut in struts.iteritems():
		strut['Type'] = strutType(strut)

#calculate the length of a strut
def strutLength(strut, nodes):
	#assemble node IDs form dict
	NodeIDs = {}
	for ID, node in nodes.iteritems():
		NodeIDs[node['ID']] = ID

	a0 = nodes[NodeIDs[strut['StartNode']]]['X']
	a1 = nodes[NodeIDs[strut['StartNode']]]['Z']
	a  = np.array([a0, a1])

	b0 = nodes[NodeIDs[strut['EndNode']]]['X']
	b1 = nodes[NodeIDs[strut['EndNode']]]['Z']
	b  = np.array([b0, b1])

	return np.linalg.norm(a - b)

#calculate the local to global angle of a strut
def strutAngle(strut, nodes):
	#assemble node IDs form dict
	NodeIDs = {}
	for ID, node in nodes.iteritems():
		NodeIDs[node['ID']] = ID

	X0 = nodes[NodeIDs[strut['StartNode']]]['X']
	Z0 = nodes[NodeIDs[strut['StartNode']]]['Z']

	X1 = nodes[NodeIDs[strut['EndNode']]]['X']
	Z1 = nodes[NodeIDs[strut['EndNode']]]['Z']
	
	v1 = np.array([X1 - X0, Z1 - Z0])
	v2 = np.array([1, 0])

	cosang = np.dot(v1, v2)
	sinang = np.linalg.norm(np.cross(v1, v2))
	
	angle = 360 - np.rad2deg(np.arctan2(sinang, cosang))

	return angle

#determine type of strut
def strutType(strut):
	EndHinge = strut['EndHinge']
	StartHinge = strut['StartHinge']

	if StartHinge == 1 and EndHinge == 1:
		return '3'
	elif StartHinge == 0 and EndHinge == 1:
		return '2a'
	elif StartHinge == 1 and EndHinge == 0:
		return '2b'
	elif StartHinge == 0 and EndHinge == 0:
		return '1'
