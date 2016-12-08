from optparse import OptionParser
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

	parser.add_option("-N", "--NodeFile",
										action="store",
										dest="nodeFile",
										default='Input_nodes.csv',
										help="CSV file with node definitions")

	parser.add_option("-S", "--StrutFile",
										action="store",
										dest="strutFile",
										default='Input_struts.csv',
										help="CSV file with strut definitions")

	parser.add_option("-C", "--ConstraintFile",
										action="store",
										dest="constFile",
										default='Input_constraints.csv',
										help="CSV file with constraint definitions")

	parser.add_option("-L", "--StrutLoadFile",
										action="store",
										dest="strutLoadFile",
										default='Input_strutLoads.csv',
										help="CSV file with strut load definitions")

	parser.add_option("-F", "--NodeLoadFile",
										action="store",
										dest="nodeLoadFile",
										default='Input_nodeLoads.csv',
										help="CSV file with node load definitions")

	parser.add_option("-T",
										action="store_true",
										dest="genTemplates",
										help="Generate csv input template files")

################################################################################
#		Output files 																															 #
################################################################################

	parser.add_option("-D", "--DisplacementVectorFile",
										action="store",
										dest="displacementVectorFile",
										default='displacement.csv',
										help="Destination path to save the displacement vector csv file")

################################################################################
#		graphics																																	 #
################################################################################

	parser.add_option("-s", "--Scale",
										action="store",
										dest="scale",
										default=2.0,
										help="Scales plot elements")

	parser.add_option("-P", "--SavePlot",
										action="store",
										dest="savePlot",
										default=False,
										help="Destination path to save the system plot. Supported filetypes: .png, .pdf")

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

	print S_G

	K = assemble_global_K_I(nodes, struts)
	apply_constraints(K, struts, nodes, constraints)

	if sp.det(K) == 0:
		print('System is kinematic (det(K)=0)!')
		exit()

	if countConst(constraints) < 3:
		print('System is kinematic (n < 3)!')
		exit()

	d = solver(K, S_G, constraints, nodes)

	print d

	calc_local_forces(nodes, struts, d)

	writeDisplacements(options.displacementVectorFile, d, nodes)

	drawSystem(nodes, struts, constraints, d, options.scale, options.savePlot)
		
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