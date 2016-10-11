def nodeIDtoName(id, nodes):
	return nodes[id]["ID"]

def nodeNameToID(name, nodes):
	NodeIDs = {}
	for ID, node in nodes.iteritems():
		NodeIDs[node['ID']] = ID

	return NodeIDs[name]