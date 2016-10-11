import csv
import numpy as np
from util import *

def writeDisplacements(filename, d, nodes):
	fieldnames = ["Node", "x", "z", "r"]
	
	with open(filename + '.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter = ';')
		writer.writerow(fieldnames)

		_d = [d[n:n+3] for n in range(0, len(d), 3)]

		for ID, vec in enumerate(_d):
			row = [nodeIDtoName(ID, nodes), vec[0], vec[1], vec[2]]
			writer.writerow(row)