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
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.clock import Clock

from src.DragGrid import DragGrid
from src.FlowChartNode import FlowChartNode

Builder.load_file('flowchartwidget.kv')

class FlowchartExampleWidget(BoxLayout):
    drag_grid=ObjectProperty(None)
        
class FlowchartExampleApp(App):
    def build(self):
        root = FlowchartExampleWidget()
        lbl = Label(text='Test')
        drag = FlowChartNode(app=self, grid=root.drag_grid, cell=root.drag_grid.cells[0], label=lbl)
        root.drag_grid.cells[0].add_widget(drag)
        root.drag_grid.cells[0].nodes.append(drag)
        return root
        
    def update_connectors(self, node, connector):
        #node: the flow chart node being updated
        #connector: the connector being updated
        pass
    
    def add_flowchart_node(self, cell, label):
        #cell: the cell to add the flowchart node to
        #label: the label to use for the flowchart node
        pass
  
if __name__ == '__main__':
    FlowchartExampleApp().run()