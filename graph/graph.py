from .node import Node
from .edge import Edge


class Graph():
	def __init__(self):
		self.__g = {}
		self.__e = []

	def add_node(self, label):
		self.__g[label] = Node(label)

	def add_edge(self,a, b):
		if a not in self.__g or b not in self.__g:
			raise ValueError("Node is not present in graph")
			

		u = self.__g[a]
		v = self.__g[b]

		if u == v:
			return 

		edge = Edge(u,v)
		self.__e.append(edge)

		u.add_edge(edge)
		v.add_edge(edge)

	def remove_node(self,x):
		if x not in self.__g:
			raise ValueError(x + " is not in graph")
			 
		u = self.__g[x]
		adj_list = u.get_adjacent()
		for el in adj_list:
			v = self.__g[el]
			for edge in v.edges:
				if edge.u == u or edge.v == u:
					v.edges.remove(edge)
				
		del self.__g[x]


	def remove_edge(self,a,b):
		if a not in self.__g or b not in self.__g:
			raise ValueError(f"{a} or {b} is not present in graph")
			

		u = self.__g[a]
		v = self.__g[b]



		edge = self.get_edge(a,b)
		if edge == None:
			raise ValueError("Edge does not exist")
		self.__e.remove(edge)
		u.remove_edge(edge)
		v.remove_edge(edge)







	def get_node(self,label):
		return self.__g[label]

	def get_edge(self,a,b):
		if a not in self.__g or b not in self.__g:
			raise ValueError(f"{a} or {b} is not present in graph")
			

		u = self.__g[a]
		v = self.__g[b]

		for edge in self.__e:
			if edge.u == u and edge.v == v or edge.u == v and edge.v == u:
				return edge

	def adjacent(self,a,b):
		u = self.__g[a]
		v = self.__g[b]
		if b in u.get_adjacent():
			return True
		return False

	def __str__(self):
		
		return ' '.join(self.__g.keys())







