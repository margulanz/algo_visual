
class Node():
	def __init__(self, label):
		self.__label = label
		self.__edges = []

	def add_edge(self,edge):
		self.__edges.append(edge)


	def remove_edge(self,edge):
		self.__edges.remove(edge)

	def get_adjacent(self):
		lst = []
		for i in self.__edges:
			if i.u == self:
				lst.append(str(i.v))
			else:
				lst.append(str(i.u))
		return lst

	def __str__(self):
		return self.__label




