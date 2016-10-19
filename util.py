def nodeIDtoName(id, nodes):
	return nodes[id]["ID"]

def nodeNameToID(name, nodes):
	for ID, node in nodes.iteritems():
		if node['ID'] == name:
			return ID