from optparse import OptionParser, OptionGroup
from input import *
from output import *
from matrices import *
from load_vectors import *
from solver import *
import scipy.linalg as sp
import numpy as np
from graphics import *

version = 0.1

def main():

	parser = OptionParser(usage="usage: %prog [options]", version="%prog " + str(version))

################################################################################
#		Input files 																															 #
################################################################################

	group = OptionGroup(parser, "Input files")

	group.add_option("-N", "--NodeFile",
										type="string",
										action="store",
										dest="nodeFile",
										default='Input_nodes.csv',
										help="CSV file with node definitions")

	group.add_option("-S", "--StrutFile",
										type="string",
										action="store",
										dest="strutFile",
										default='Input_struts.csv',
										help="CSV file with strut definitions")

	group.add_option("-C", "--ConstraintFile",
										type="string",
										action="store",
										dest="constFile",
										default='Input_constraints.csv',
										help="CSV file with constraint definitions")

	group.add_option("-L", "--StrutLoadFile",
										type="string",
										action="store",
										dest="strutLoadFile",
										default='Input_strutLoads.csv',
										help="CSV file with strut load definitions")

	group.add_option("-F", "--NodeLoadFile",
										type="string",
										action="store",
										dest="nodeLoadFile",
										default='Input_nodeLoads.csv',
										help="CSV file with node load definitions")

	group.add_option("-T",
										action="store_true",
										dest="genTemplates",
										help="Generate csv input template files")

	parser.add_option_group(group)

################################################################################
#		Output files 																															 #
################################################################################

	group = OptionGroup(parser, "Output files")

	group.add_option("-D", "--DisplacementVectorFile",
										type="string",
										action="store",
										dest="displacementVectorFile",
										default='displacement.csv',
										help="Destination path to save the displacement vector csv file")

	parser.add_option_group(group)

################################################################################
#		graphics																																	 #
################################################################################

	group = OptionGroup(parser, "Graphics options")

	group.add_option("-s", "--Scale",
										type="float",
										action="store",
										dest="scale",
										default=2.0,
										help="Scales plot elements")

	group.add_option("-P", "--SavePlot",
										type="string",
										action="store",
										dest="savePlot",
										default=False,
										help="Destination path to save the system plot. Supported filetypes: .png, .pdf")

	parser.add_option_group(group)

################################################################################
#		debug																																	 #
################################################################################

	group = OptionGroup(parser, "Debug options")

	group.add_option("-d", "--Debug",
										action="store_true",
										dest="debug",
										help="Print debug outputs")

	parser.add_option_group(group)

################################################################################

	(options, args) = parser.parse_args()

	if options.genTemplates:
		genTemplate('nodesTemplate.csv', nodesTypeTemplate)
		genTemplate('strutsTemplate.csv', strutsTypeTemplate)
		genTemplate('constraintTemplate.csv', constraintTypeTemplate)
		genTemplate('strutLoadTemplate.csv', strutLoadTypeTemplate)
		genTemplate('nodeLoadTemplate.csv', nodeLoadTypeTemplate)
		exit()

	nodes = readCSV(options.nodeFile, nodesTypeTemplate)
	struts = readCSV(options.strutFile, strutsTypeTemplate)
	deleteFreeNodes(nodes, struts)
	constraints = readCSV(options.constFile, constraintTypeTemplate)
	strutLoads = readCSV(options.strutLoadFile, strutLoadTypeTemplate)
	nodeLoads = readCSV(options.nodeLoadFile, nodeLoadTypeTemplate)

	checkStrutNodes(nodes, struts)
	checkConstraintNodes(nodes, constraints)
	checkStrutLoads(struts, strutLoads)
	checkNodeLoads(nodes, nodeLoads)

	getStrutLength(nodes, struts)
	getStrutAngle(nodes, struts)
	getStrutType(struts)
	assemble_S_L(strutLoads, struts, nodes)

	S_G = assemble_S_G(nodeLoads, struts, nodes)

	# debug
	printDebugMatrix("S_G", S_G, options.debug)

	K = assemble_global_K_I(nodes, struts)
	apply_constraints(K, struts, nodes, constraints)

	# debug
	printDebugMatrix("K", K, options.debug)

	if sp.det(K) == 0:
		print('System is kinematic (det(K)=0)!')
		exit()

	if countConst(constraints) < 3:
		print('System is kinematic (n < 3)!')
		exit()

	d = solver(K, S_G, constraints, nodes)
	calc_local_forces(nodes, struts, d)

	# debug
	printDebugMatrix("d", d, options.debug)
	printDebugStrutAttr("K", "K", struts, options.debug)
	printDebugStrutAttr("S_l", "Sl", struts, options.debug)

	writeDisplacements(options.displacementVectorFile, d, nodes)
	drawSystem(nodes, struts, constraints, strutLoads, nodeLoads, d, float(options.scale), options.savePlot)

if __name__ == '__main__':
	main()

