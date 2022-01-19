from kivy.app import App
from kivy.graphics import Color, Ellipse, Line,Rectangle
from kivy.properties import StringProperty


from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button


import networkx as nx
from node import NodesLayout,Node
from edge import Edge






# Graph Editor Layout Implementation
class GraphEditor(FloatLayout):
	def __init__(self,**kwargs):
		super(GraphEditor,self).__init__(**kwargs)
		self.nodes = []
		self.edges = []
		self.max_num_of_nodes = 20
		self.add_vertex = False
		self.add_edge = False
		self.G = nx.Graph()
		# Should draw background 
		#self.canvas.add(Color(255,255,255))
		#self.canvas.add(Rectangle(size = (700,525)))
		# Should be done in order to place lines behind nodes
		self.nodes_layout = NodesLayout()
		self.add_widget(self.nodes_layout)

	def on_touch_down(self,touch):
		alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		radius = 25
		# Adding new nodes
		if touch.spos[1] <=.78 and self.add_vertex == True:

			if len(self.nodes) >= self.max_num_of_nodes:
				return
			curr_label = alphabet[len(self.nodes)]
			new_node = Node(label = curr_label,pos = (touch.pos[0],touch.pos[1]),size_hint_y = None,height = 50,size_hint_x = None,width = 50)
			self.nodes_layout.add_widget(new_node)
			self.nodes.append(new_node)
			self.G.add_node(new_node.label)
			new_node.draw_node(touch.pos)	

		# Adding new edges
		if touch.spos[1] <=.78 and self.add_edge == True:
			# If we are adding edge, we should continue finding children widget
			super(GraphEditor, self).on_touch_down(touch)	
			selected_num = 0
			self.selected_nodes = []
			for node in self.nodes:
				if node.selected == True:
					self.selected_nodes.append(node)
					selected_num+=1
				if selected_num == 2:
					for edge in self.G.edges():
						if (self.selected_nodes[0].label in edge) and (self.selected_nodes[1].label in edge):
							print("Already present")
							return
					self.new_edge = Edge()

					window = FloatLayout()
					window.add_widget(Label(text = "Weight: "))
					self.input = TextInput(multiline = False,size_hint = (.2,None),height = 30,pos_hint = {'x':.38,'y':.4})
					window.add_widget(self.input)
					window.add_widget(Button(text = "Submit",size_hint = (.2,None),height = 30,pos_hint = {'x':.38,'y':.2},on_press = self.create_edge))
					self.popup = Popup(title = "Enter value",content = window)
					self.popup.open()
					break


					
	def create_edge(self,value):
		self.new_edge.weight = int(self.input.text)
		self.G.add_edge(self.selected_nodes[0].label,self.selected_nodes[1].label,weight = self.new_edge.weight)
		self.activate_vertex_addition(None)
		self.activate_edge_addition(None)
		
		
		self.add_widget(self.new_edge)
		self.new_edge.nodes += [self.selected_nodes[0],self.selected_nodes[1]]


		self.new_edge.draw_edge(self.selected_nodes[0],self.selected_nodes[1])
		self.edges.append(self.new_edge)


		self.remove_widget(self.nodes_layout)
		self.add_widget(self.nodes_layout)
		self.popup.dismiss()	
		self.activate_vertex_addition(None)
		self.activate_edge_addition(None)		
				


			

	def activate_vertex_addition(self,value):
		for node in self.nodes:
			node.selected = False
			node.draw_node(node.pos)
		for edge in self.edges:
			edge.selected = False
			edge.draw_edge(edge.nodes[0],edge.nodes[1])
		self.add_vertex = True
		self.add_edge = False
		
	def activate_edge_addition(self,value):
		self.add_edge = True
		self.add_vertex = False
	def clear_canvas(self, obj):
		for node in self.nodes:
			self.nodes_layout.remove_widget(node)
		self.nodes_layout.canvas.clear()
		self.nodes = []
		self.G.clear()
		self.canvas.clear()
		self.canvas.add(Color(255,255,255))
		self.canvas.add(Rectangle(size = self.size))
		self.remove_widget(self.nodes_layout)
		self.add_widget(self.nodes_layout)