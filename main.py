

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



from edge import Edge
from node import Node
from graph_editor import GraphEditor

def enumerate2(xs, start=0, step=1):
    for x in xs:
        yield (start, x)
        start += step



		






		
			
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

		# Should add my own implementations
		node_order = list(nx.dfs_edges(self.editor.G,source = self.input.text))
		self.traversal(node_order)

		
			
	def bfs(self,value):

		# Should add my own implementations
		node_order = list(nx.bfs_edges(self.editor.G,source = self.input.text))
		self.traversal(node_order)

		
	def traversal(self,node_order):
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

	def path(self,node_order):
		self.editor.activate_vertex_addition(None)
		self.editor.activate_edge_addition(None)
		for count,edge in enumerate2(node_order,0,.5): # edge = (Node_1, Node_2)
			node_a = self.return_node(edge[0])
			node_a.selected = True
			Clock.schedule_once(partial(node_a.draw_node,node_a.pos),count)
		self.editor.add_edge = False	
		self.popup.dismiss()
	def shortest_path(self,value):
		
		self.dropdown.dismiss()
		# Should add my own implementations
		node_order = list(nx.shortest_path(self.editor.G,source = self.input_source.text,target = self.input_target.text,weight = 'weight',method='dijkstra')) # returns list
		self.path(node_order)


		


		

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