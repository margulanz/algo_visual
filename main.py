

import networkx as nx
from kivy.app import App
from kivy.clock import Clock
from random import random
import time
from functools import partial



# UIX
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Ellipse, Line,Rectangle
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


def enumerate2(xs, start=0, step=1):
    for x in xs:
        yield (start, x)
        start += step


# Edge Widget Implementation
class Edge(Widget):
	def __init__(self,**kwargs):
		super(Edge,self).__init__(**kwargs)
		self.nodes = []
		self.selected = False
		self.weight = 1
	def draw_edge(self,node_a,node_b,dt = None):
		if not self.selected:
			with self.canvas:
				Color(0,0,0)
				Line(points = [node_a.pos[0],node_a.pos[1],node_b.pos[0],node_b.pos[1]],width=2)
				Label(font_size = '20sp',size_hint = (1,1),text = str(self.weight),pos = ((node_a.pos[0]+node_b.pos[0]-100)/2,(node_a.pos[1]+node_b.pos[1]-50)/2),color = (0,1,1,1))
		else:
			with self.canvas:
				Color(1,0,0)
				Line(points = [node_a.pos[0],node_a.pos[1],node_b.pos[0],node_b.pos[1]],width=2)
		
# Node Widget Implementation	
class Node(Widget):
	label = StringProperty("")
	def __init__(self,**kwargs):
		super(Node,self).__init__(**kwargs)
		self.selected = False
	def on_touch_down(self,touch):
		if (self.pos[0]-25<=touch.pos[0]<=self.pos[0]+self.size[0]-25 and self.pos[1]-25<=touch.pos[1]<=self.pos[1]+self.size[1]-25):
			self.selected = not self.selected
			self.canvas.clear()
			self.draw_node(self.pos)
			return True
	def draw_node(self,pos,dt = None):
		radius = 25
		if self.selected:
			color = (249/255,19/255,38/255)
		else:
			color = (146/255,170/255,217/255)
		with self.canvas:
			Color(*color)
			Ellipse(pos = (pos[0]-radius,pos[1]-radius),size = (radius*2,radius*2))
		self.add_widget(Label(font_size = '35sp',size_hint = (1,1),text = self.label,pos = (pos[0]-2*radius,pos[1]-2*radius),color = (0,0,0,1)))


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

# Node Layout that contains all node widgets
class NodesLayout(Widget):
	def __init__(self,**kwargs):
		super(NodesLayout,self).__init__(**kwargs)	
		
			
# MAIN
class MainApp(App):
	def build(self):
		# Graph Editor
		self.editor = GraphEditor()

		# Dropdown button
		self.dropdown = DropDown()
		self.dropdown.add_widget(Button(text = "DFS",size_hint_y=None, height=20,on_release = self.window_traversal))
		self.dropdown.add_widget(Button(text = "BFS",size_hint_y=None, height=20,on_release = self.window_traversal))
		self.dropdown.add_widget(Button(text = "Dijkstra's algorithm (shortest Path)",size_hint_y=None, height=20,on_release = self.window_traversal))
		
		Layout = BoxLayout(orientation = 'vertical')

		# Top bar
		top_bar = BoxLayout(orientation = 'horizontal',size_hint = (1,.1))
		top_bar.add_widget(Button(id = "vertex",text = "Add vertex",height = 10,on_press = self.button_pressed))
		top_bar.add_widget(Button(id = "edge",text = "Add Edge",height = 10,on_press = self.button_pressed))
		mainbutton = Button(text='Graph Algo')
		mainbutton.bind(on_release=self.dropdown.open)
		top_bar.add_widget(mainbutton)
		top_bar.add_widget(Button(text = "Delete",on_press=self.editor.clear_canvas))

		# Status bar
		status_bar = BoxLayout(orientation = 'horizontal',size_hint = (1,.05))
		self.status = Label(text = "Status")
		status_bar.add_widget(self.status)
		# Adding top bar and editor		
		Layout.add_widget(status_bar)
		Layout.add_widget(top_bar)
		Layout.add_widget(self.editor)

		# Output
		return Layout

	def button_pressed(self,value):
		if value.id == "vertex":
			self.editor.activate_vertex_addition(value)
			self.status.text = "Add vertex"
		elif value.id == "edge":
			self.editor.activate_edge_addition(value)
			self.status.text = "Add edge"


	def window_traversal(self,value):
		if value.text == "DFS":
			press = self.dfs
		elif value.text == "BFS":
			press = self.bfs
		elif value.text == "Dijkstra's algorithm (shortest Path)":
			window = FloatLayout()
			window.add_widget(Label(text = "Enter source: ",size_hint = (.2,None),height = 30,pos_hint = {'x':.20,'y':.4}))
			self.input_source = TextInput(multiline = False,size_hint = (.2,None),height = 30,pos_hint = {'x':.38,'y':.4})
			window.add_widget(Label(text = "Enter target: ",size_hint = (.2,None),height = 30,pos_hint = {'x':.20,'y':.3}))
			self.input_target = TextInput(multiline = False,size_hint = (.2,None),height = 30,pos_hint = {'x':.38,'y':.3})
			window.add_widget(Button(text = "submit",size_hint = (.2,None),height = 30,pos_hint = {'x':.38,'y':.2},on_press = self.shortest_path))
			window.add_widget(self.input_source)
			window.add_widget(self.input_target)
			self.popup = Popup(title = "Test",content = window)
			self.popup.open()
			self.dropdown.dismiss()
			return
		self.dropdown.dismiss()
		window = FloatLayout()
		window.add_widget(Label(text = "Enter source: "))
		self.input = TextInput(multiline = False,size_hint = (.2,None),height = 30,pos_hint = {'x':.38,'y':.4})
		window.add_widget(self.input)
		window.add_widget(Button(text = "submit",size_hint = (.2,None),height = 30,pos_hint = {'x':.38,'y':.2},on_press = press))
		self.popup = Popup(title = "Test",content = window)
		self.popup.open()

	def dfs(self,value):
		node_order = list(nx.dfs_edges(self.editor.G,source = self.input.text))
		self.editor.activate_vertex_addition(None)
		self.editor.activate_edge_addition(None)
		for count,edge in enumerate2(node_order,0,0.5):
			node_a = self.return_node(edge[0])
			node_b = self.return_node(edge[1])
			edge = self.return_edge(edge[0],edge[1])
			node_a.selected = True
			node_b.selected = True
			edge.selected = True
			Clock.schedule_once(partial(node_a.draw_node,node_a.pos),count+.5)
			Clock.schedule_once(partial(edge.draw_edge,node_a,node_b),count+1)
			Clock.schedule_once(partial(node_b.draw_node,node_b.pos),count+1)
		self.editor.add_edge = False
		self.popup.dismiss()
			
	def bfs(self,value):
		node_order = list(nx.bfs_edges(self.editor.G,source = self.input.text))
		self.editor.activate_vertex_addition(None)
		self.editor.activate_edge_addition(None)
		for count,edge in enumerate2(node_order,0,0.5):
			node_a = self.return_node(edge[0])
			node_b = self.return_node(edge[1])
			edge = self.return_edge(edge[0],edge[1])
			node_a.selected = True
			node_b.selected = True
			edge.selected = True
			Clock.schedule_once(partial(node_a.draw_node,node_a.pos),count+.5)
			Clock.schedule_once(partial(edge.draw_edge,node_a,node_b),count+1)
			Clock.schedule_once(partial(node_b.draw_node,node_b.pos),count+1)
		self.editor.add_edge = False
		self.popup.dismiss()

	def shortest_path(self,value):
		
		self.dropdown.dismiss()
		node_order = list(nx.shortest_path(self.editor.G,source = self.input_source.text,target = self.input_target.text,weight = 'weight',method='dijkstra'))
		self.editor.activate_vertex_addition(None)
		self.editor.activate_edge_addition(None)
		for count,edge in enumerate2(node_order,0,.5): # edge = (Node_1, Node_2)
			node_a = self.return_node(edge[0])
			node_a.selected = True
			Clock.schedule_once(partial(node_a.draw_node,node_a.pos),count)
		self.editor.add_edge = False	
		self.popup.dismiss()


		

	def return_node(self,label):
		for n in self.editor.nodes:
			if n.label == label:
				return n	
	
	def return_edge(self,node_a,node_b):
		node = (self.return_node(node_a),self.return_node(node_b))
		for edge in self.editor.edges:
			if node[0] in edge.nodes and node[1] in edge.nodes:
				return edge

if __name__ == '__main__':
	MainApp().run()