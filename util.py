def nodeIDtoName(id, nodes):
	return nodes[id]["ID"]

def nodeNameToID(name, nodes):
	for ID, node in nodes.iteritems():
		if node['ID'] == name:
			return ID

def getConsttraint(name, constraints):
	for ID, const in constraints.iteritems():
		if const['Node'] == name:
			return const

def getStrutLoad(name, strutLoads):
	for ID, strutLoad in strutLoads.iteritems():
		if strutLoad['Strut'] == name:
			return strutLoad