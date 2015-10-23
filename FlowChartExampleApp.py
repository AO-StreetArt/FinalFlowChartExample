# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 19:03:15 2015

@author: alex
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.clock import Clock

from src.DragGrid import DragGrid, DragGridCell
from src.FlowChartNode2 import FlowChartNode, DraggableImage

Builder.load_file('flowchartwidget.kv')

class FlowchartExampleWidget(FloatLayout):
    drag_grid=ObjectProperty(None)
        
class FlowchartExampleApp(App):
    def build(self):
        root = FlowchartExampleWidget()
        
        lbl = Label(text='Test')
        drag_label = DraggableImage(img=lbl, app=self, grid=root.drag_grid, cell=root.drag_grid.cells[0])
        drag = FlowChartNode(app=self, grid=root.drag_grid, cell=root.drag_grid.cells[0], label=drag_label)
        drag_label.node = drag
        root.drag_grid.cells[0].add_widget(drag)
        root.drag_grid.cells[0].nodes.append(drag)
        root.drag_grid.nodes.append(drag)
        
        lbl2 = Label(text='Test2')
        drag_label2 = DraggableImage(img=lbl2, app=self, grid=root.drag_grid, cell=root.drag_grid.cells[1])
        drag2 = FlowChartNode(app=self, grid=root.drag_grid, cell=root.drag_grid.cells[1], label=drag_label2)
        drag_label2.node = drag2
        root.drag_grid.cells[1].add_widget(drag2)
        root.drag_grid.cells[1].nodes.append(drag2)
        root.drag_grid.nodes.append(drag2)
        
        return root
    
    def create_connections(self, *args):
        pass
  
if __name__ == '__main__':
    FlowchartExampleApp().run()