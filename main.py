import networkx as nx
from kivy.app import App
from random import random


# UIX
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Ellipse, Line,Rectangle
from kivy.properties import StringProperty
from kivy.properties import ListProperty


G = nx.Graph()

class Node(Widget):
	label = StringProperty("")
	position = ListProperty([0,0])
	def __init__(self,**kwargs):
		super(Node,self).__init__(**kwargs)


class GraphEditor(FloatLayout):
	def __init__(self,**kwargs):
		super(GraphEditor,self).__init__(**kwargs)
		self.nodes = []
		self.max_num_of_nodes = 20
		self.add_vertex = False
		self.add_edge = False
	def on_touch_down(self,touch):
		alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		radius = 25
		if touch.spos[1] <=.78 and self.add_vertex == True:
			if len(self.nodes) >= self.max_num_of_nodes:
				return
			curr_label = alphabet[len(self.nodes)]
			new_node = Node(label = curr_label,position = [touch.pos[0]-radius,touch.pos[1]-radius])
			print(touch.pos)
			
			self.nodes.append(new_node)
			G.add_node(new_node.label)
			with self.canvas:
				color= (146/255,170/255,217/255)
				Color(*color)
				Ellipse(pos = (touch.pos[0]-radius,touch.pos[1]-radius),size = (radius*2,radius*2))

			self.add_widget(Label(size_hint = (.00625,.00625),text = new_node.label,pos = (touch.pos),color = (0,0,0,1)))
	def clear_canvas(self, obj):
		print(G)
		self.nodes = []
		G.clear()
		self.canvas.clear()
		self.canvas.add(Color(255,255,255))
		self.canvas.add(Rectangle(size = self.size))
	def activate_vertex_addition(self,value):
		self.add_vertex = True
		self.add_edge = False
		print("hello!")
	def activate_edge_addition(self,value):
		self.add_edge = True
		self.add_vertex = False
		print("bitch")
		
			

class MainApp(App):
	def build(self):
		# Graph Editor
		self.editor = GraphEditor(size = (1,1))

		# Dropdown button
		self.dropdown = DropDown()
		self.dropdown.add_widget(Button(text = "DFS",size_hint_y=None, height=20,on_release = self.dropdown.dismiss))
		self.dropdown.add_widget(Button(text = "BFS",size_hint_y=None, height=20,on_release = self.dropdown.dismiss))
		self.dropdown.add_widget(Button(text = "Soon...",size_hint_y=None, height=20,on_release = self.dropdown.dismiss))
		
		Layout = BoxLayout(orientation = 'vertical')

		# Top bar
		top_bar = BoxLayout(orientation = 'horizontal',size_hint = (1,.1))
		top_bar.add_widget(Button(id = "vertex",text = "Add vertex",height = 10,on_press = self.button_pressed))
		top_bar.add_widget(Button(id = "edge",text = "Add Edge",height = 10,on_press = self.button_pressed))
		mainbutton = Button(text='Graph Algo')
		mainbutton.bind(on_release=self.dropdown.open)
		top_bar.add_widget(mainbutton)
		top_bar.add_widget(Button(text = "del",on_press=self.editor.clear_canvas))

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

	

if __name__ == '__main__':
	MainApp().run()