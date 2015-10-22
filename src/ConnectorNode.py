# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 21:22:50 2015

@author: alex
"""

from DraggableConnector import DraggableConnector, SimpleConnectorButton
from Connector import Connector
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.logger import Logger

class ConnectorNode(BoxLayout):
    
    #The app currently working in
    app = ObjectProperty(None)
    
    #The Grid being added to
    grid = ObjectProperty(None)
    
    #The cell the button occupies
    cell = ObjectProperty(None) 
    
    #The flow chart node the connector node is in
    node = ObjectProperty(None)

    #The color of the connection lines in rgb
    connector_color = ListProperty([1, 1, 1])
    
    #Internal Properties
    #Property to set the list of connected nodes
    connected_nodes = ListProperty([])   
    
    #The Center Widget
    center_node = ObjectProperty(None)
    
    #Internal property to track the connections
    connect = ListProperty([])
    
    def __init__(self, **kwargs):
        super(ConnectorNode, self).__init__(**kwargs)
        #create the center button & bind the properties
        Clock.schedule_once(self.build_center)
        
    def build_center(self, *args):
        c_node = SimpleConnectorButton(grid=self.grid, cell=self.cell, node=self)
        Logger.debug('Flowchart: ConnectorNode: Connector Node initialized with grid %s, cell %s, and node %s' % (self.grid, self.cell, self))
        c_node.bind(pos=self.set_front, on_press=self.press_front)
        self.center_node = c_node
        self.add_widget(self.center_node)
        
    def set_front(self, *args):
        for con in self.connect:
            con.front = self.center_node.center
        
    def set_back(self, *args):
        i=0
        for con in self.connect:
            con.back = self.connected_nodes[i].center
            i+=1
        
    def press_front(self, *args):
        #Add the option nodes and connectors to the widget if it's closed
        #Otherwise, close the widget
        if len(self.connect) == 0:
            for option in self.connected_nodes:
                connector = MenuConnector(line_color=self.connector_color)
                self.connect.append(connector)
                
            Logger.debug('Flowchart: ConnectorNode: Connections Created')
        #Add a new connector and a new draggable image lists
        connector = Connector(line_color=self.connector_color)
        self.connect.append(connector)
        
        image = Image(source='drag_node_small.png')
        drag = DraggableConnector(img=image, app=self.app, grid=self.grid, cell=self.grid.get_next_cell(self.cell.row, self.cell.col), node=self.node)
        Logger.debug('Flowchart: ConnectorNode: Draggable Connector initialized with app %s, grid %s, cell %s, and node %s' % (self.app, self.grid, self.cell, self))
        self.connected_nodes.append(drag)
        
        self.clear_widgets()
        cel = self.grid.get_next_cell(self.cell.row, self.cell.col)
        cel.clear_widgets()
        for con in self.connect:
            cel = self.grid.get_next_cell(self.cell.row, self.cell.col)
            cel.add_widget(con)
        for option in self.connected_nodes:
            option.bind(pos=self.set_back)
            cel = self.grid.get_next_cell(self.cell.row, self.cell.col)
            cel.add_widget(option)
        self.add_widget(self.center_node)
            
        for con in self.connect:
            con.front = self.center_node.center