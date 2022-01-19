from kivy.app import App
from kivy.graphics import Color, Ellipse, Line,Rectangle
from kivy.properties import StringProperty


from kivy.uix.widget import Widget
from kivy.uix.label import Label

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