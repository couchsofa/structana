nodesTypeTemplate 		= [	('ID' , str),
							('X' , float),
							('Z' , float)]

strutsTypeTemplate 		= [	('ID' , str),
							('StartNode' , str),
							('StartHinge' , int),
							('EndNode' , str),
							('EndHinge' , int),
							('E' , float),
							('A' , float),
							('I' , float)]

constraintTypeTemplate 	= [	('Node' , str),
							('x' , int),
							('z' , int),
							('r' , int)]

strutLoadTypeTemplate 	= [	('Strut' , str),
							('Type' , int),
							('x1' , float),
							('x2' , float),
							('q' , float),
							('F' , float),
							('M' , float)]

nodeLoadTypeTemplate 	= [	('Node' , str),
							('Fx' , float),
							('Fz' , float),
							('M' , float)]