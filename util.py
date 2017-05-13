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

def getStrutByName(name, struts):
	for ID, strut in struts.iteritems():
		if strut['ID'] == name:
			return strut

def printDebugMatrix(Name, M, debug):
	if debug:
		print Name + ": "
		print "################################################################################"
		print M
		print "################################################################################"
		print ""

def printDebugStrutAttr(Name, Attr, struts, debug):
	if debug:
		for ID, strut in struts.iteritems():
			print "Strut " + strut["ID"] + " [" + Name + "]: "
			print "################################################################################"
			print strut[Attr]
			print "################################################################################"
			print ""