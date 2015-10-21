# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:33:59 2015

Flow Chart Node

@author: alex
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from DraggableLabel import DraggableLabel
from ConnectorNode import ConnectorNode
from kivy.properties import ObjectProperty, ListProperty
from kivy.clock import Clock
from kivy.logger import Logger

class FlowChartNode(BoxLayout):
    
    #The label for the widget
    #Exposed so that any widget can be added
    label = ObjectProperty(None)
    
    #The app being added to
    app = ObjectProperty(None)
    
    #The Grid the widget is in
    grid = ObjectProperty(None)
    
    #The cell the widget is currently in
    cell = ObjectProperty(None)
    
    #Internal Properties
    #The connector node for the widget
    connector = ObjectProperty(None)
    
    #The receiver for the widget
    receiver = ObjectProperty(None)
    
    #A list of forward connections to other nodes
    connections = ListProperty([])
    
    def __init__(self, **kwargs):
        
        super(FlowChartNode, self).__init__(**kwargs)
        
        con = ConnectorNode(app=self.app, grid=self.grid, cell=self.cell)
        Logger.debug('Flowchart: ConnectorNode: Connector Node initialized with app %s, grid %s, and cell %s' % (self.app, self.grid, self.cell))
        rec = Image(source='src/img/drag_node_small.png')
        self.connector = con
        self.receiver = rec

        Clock.schedule_once(self.build_widget)
        
    def build_widget(self, *args):
        buf1 = BoxLayout(size_hint=[0.25, 0.3])
        buf2 = BoxLayout(size_hint=[0.25, 0.3])
        buf3 = BoxLayout(size_hint=[0.25, 0.3])
        buf4 = BoxLayout(size_hint=[0.25, 0.3])
        
        self.connector.size_hint=[0.5, 0.3]
        self.receiver.size_hint=[0.5, 0.3]
        self.label.size_hint=[1, 0.4]
        
        self.orientation='vertical'
        self.add_widget(buf1)
        self.add_widget(self.receiver)
        self.add_widget(buf2)
        self.add_widget(self.label)
        self.add_widget(buf3)
        self.add_widget(self.connector)
        self.add_widget(buf4)