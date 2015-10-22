# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:33:59 2015

Flow Chart Node

@author: alex
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
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
    
    buf = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        
        super(FlowChartNode, self).__init__(**kwargs)
        
        con = ConnectorNode(app=self.app, grid=self.grid, cell=self.cell, node=self)
        Logger.debug('Flowchart: ConnectorNode: Connector Node initialized with app %s, grid %s, and cell %s' % (self.app, self.grid, self.cell))
        rec = Image(source='src/img/drag_node_small.png')
        self.connector = con
        self.receiver = rec

        Clock.schedule_once(self.build_widget)
        
    def build_widget(self, *args):
        row1 = BoxLayout(size_hint=[1, 0.3])
        row2 = BoxLayout(size_hint=[1, 0.4])
        row3 = BoxLayout(size_hint=[1, 0.3])
        buf1 = BoxLayout(size_hint=[0.25, 1])
        buf2 = BoxLayout(size_hint=[0.25, 1])
        buf3 = BoxLayout(size_hint=[0.25, 1])
        buf4 = BoxLayout(size_hint=[0.25, 1])
        self.buf=buf4
        
        self.connector.size_hint=[0.5, 1]
        self.receiver.size_hint=[0.5, 1]
        self.label.size_hint=[1, 1]
        
        self.orientation='vertical'
        row1.orientation='horizontal'
        row2.orientation='horizontal'
        row3.orientation='horizontal'
        
        row1.add_widget(buf1)
        row1.add_widget(self.receiver)
        row1.add_widget(buf2)
        row2.add_widget(self.label)
        row3.add_widget(buf3)
        row3.add_widget(self.connector)
        row3.add_widget(buf4)
        
        self.add_widget(row1)
        self.add_widget(row2)
        self.add_widget(row3)
        
    def build_widget_no_connector(self, *args):
        row1 = BoxLayout(size_hint=[1, 0.3])
        row2 = BoxLayout(size_hint=[1, 0.4])
        row3 = BoxLayout(size_hint=[1, 0.3])
        buf1 = BoxLayout(size_hint=[0.25, 1])
        buf2 = BoxLayout(size_hint=[0.25, 1])
        buf3 = BoxLayout(size_hint=[0.25, 1])
        buf4 = BoxLayout(size_hint=[0.25, 1])
        self.buf=buf4
        
        self.connector.size_hint=[0.5, 1]
        self.receiver.size_hint=[0.5, 1]
        self.label.size_hint=[1, 1]
        
        self.orientation='vertical'
        row1.orientation='horizontal'
        row2.orientation='horizontal'
        row3.orientation='horizontal'
        
        row1.add_widget(buf1)
        row1.add_widget(self.receiver)
        row1.add_widget(buf2)
        row2.add_widget(self.label)
        row3.add_widget(buf3)
        
        self.add_widget(row1)
        self.add_widget(row2)
        self.add_widget(row3)
        
    def clear_all_widgets(self, *args):
        self.clear_widgets()
        self.connector.parent.clear_widgets()
        self.receiver.parent.clear_widgets()
        self.label.parent.clear_widgets()
        