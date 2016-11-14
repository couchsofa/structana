#from optparse import OptionParser
from input import *
from output import *
from matrices import *
from load_vectors import *
from solver import *
import scipy.linalg as sp
import numpy as np
import graphics

def main():
	nodes = readCSV('Input_nodes.csv', nodesTypeTemplate)
	struts = readCSV('Input_struts.csv', strutsTypeTemplate)
	deleteFreeNodes(nodes, struts)
	constraints = readCSV('Input_constraints.csv', constraintTypeTemplate)
	strutLoads = readCSV('Input_strutLoads.csv', strutLoadTypeTemplate)
	nodeLoads = readCSV('Input_nodeLoads.csv', nodeLoadTypeTemplate)

	checkStrutNodes(nodes, struts)
	checkConstraintNodes(nodes, constraints)
	checkStrutLoads(struts, strutLoads)
	checkNodeLoads(nodes, nodeLoads)

	getStrutLength(nodes, struts)
	getStrutAngle(nodes, struts)
	getStrutType(struts)
	assemble_S_L(strutLoads, struts, nodes)

	S_G = assemble_S_G(nodeLoads, struts, nodes)

	K = assemble_global_K_I(nodes, struts)
	apply_constraints(K, struts, nodes, constraints)

	#graphics.renderSystem(nodes, struts, constraints, size=30)


	print K


	if sp.det(K) == 0:
		print('System is kinematic (det(K)=0)!')
		exit()

	if countConst(constraints) < 3:
		print('System is kinematic (n < 3)!')
		exit()

	d = solver(K, S_G, constraints, nodes)

	print d
	print S_G
	print struts

	for ID, strut in struts.iteritems():
		print "Strut " + str(ID) + " is of type: " + strut['Type']

	calc_local_forces(nodes, struts, d)


	writeDisplacements("displacement", d, nodes)
		
#		parser = OptionParser(usage="usage: %prog [options] filename",
#													version="%prog 1.0")
#		parser.add_option("-x", "--xhtml",
#											action="store_true",
#											dest="xhtml_flag",
#											default=False,
#											help="create a XHTML template instead of HTML")
#		parser.add_option("-c", "--cssfile",
#											action="store", # optional because action defaults to "store"
#											dest="cssfile",
#											default="style.css",
#											help="CSS file to link",)
#		(options, args) = parser.parse_args()
#
#		if len(args) != 1:
#				parser.error("wrong number of arguments")
#
#		print options
#		print args



if __name__ == '__main__':
	main()