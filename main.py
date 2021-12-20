import networkx as nx
from kivy.app import App
from random import random


# UIX
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Ellipse, Line,Rectangle

class GraphEditor(Widget):
	def on_touch_down(self,touch):
		if touch.pos[1] <=544:
			with self.canvas:
				color=255,255,0
				Color(*color)
				Ellipse(pos = (touch.pos[0]-25,touch.pos[1]-25),size = (50,50))

class MainApp(App):
	def build(self):
		self.editor = GraphEditor()


		dropdown = DropDown()
		dropdown.add_widget(Button(text = "DFS",size_hint_y=None, height=44,on_release = dropdown.dismiss))
		dropdown.add_widget(Button(text = "BFS",size_hint_y=None, height=44,on_release = dropdown.dismiss))
		Layout = BoxLayout(orientation = 'vertical')

		top_bar = BoxLayout(orientation = 'horizontal',size_hint = (1,.1))
		top_bar.add_widget(Button(text = "Add vertex",height = 10))
		top_bar.add_widget(Button(text = "Add Edge",height = 10))
		mainbutton = Button(text='Graph Algo')
		mainbutton.bind(on_release=dropdown.open)
		top_bar.add_widget(mainbutton)
		top_bar.add_widget(Button(text = "del",on_press=self.clear_canvas))

		
		Layout.add_widget(top_bar)
		Layout.add_widget(self.editor)
		return Layout

	def clear_canvas(self, obj):
		self.editor.canvas.clear()
		self.editor.canvas.add(Color(255,255,255))
		self.editor.canvas.add(Rectangle(size = self.editor.size))
	

if __name__ == '__main__':
	MainApp().run()