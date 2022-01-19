from kivy.app import App
from kivy.graphics import Color, Ellipse, Line,Rectangle
from kivy.properties import StringProperty


from kivy.uix.widget import Widget
from kivy.uix.label import Label



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

# Node Layout that contains all node widgets
class NodesLayout(Widget):
	def __init__(self,**kwargs):
		super(NodesLayout,self).__init__(**kwargs)	