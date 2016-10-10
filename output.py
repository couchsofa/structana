import csv
import numpy as np

def writeDisplacements(filename, d, nodes):
	#assemble node IDs form dict
	NodeIDs = {}
	for ID, node in nodes.iteritems():
		NodeIDs[ID] = node['ID']

	fieldnames = ["Node", "x", "z", "r"]
	
	with open(filename + '.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter = ';')
		writer.writerow(fieldnames)

		_d = [d[n:n+3] for n in range(0, len(d), 3)]

		for ID, vec in enumerate(_d):
			row = [NodeIDs[ID], vec[0], vec[1], vec[2]]
			writer.writerow(row)