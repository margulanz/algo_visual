class Edge():
	def __init__(self,a, b):
		self.u = a 
		self.v = b
	def __str__(self):
		return str(self.u) + "<->" + str(self.v)