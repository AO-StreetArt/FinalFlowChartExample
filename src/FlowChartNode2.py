# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:31:48 2015

2nd Version Flowchart Node

@author: alex barry
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from Connector import Connector
from Magnet import Magnet
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.logger import Logger

#This class defines a draggable image
class DraggableImage(Magnet):
    img = ObjectProperty(None, allownone=True)
    app = ObjectProperty(None)
    grid = ObjectProperty(None)
    cell = ObjectProperty(None)
    
    double_press=ListProperty([0,0])
    is_set=BooleanProperty(False)
    has_button=BooleanProperty(False)

    def on_img(self, *args):
        self.clear_widgets()
        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.double_press=touch.pos
                if self.is_set:
                    self.is_set=False
                else:
                    self.is_set=True
                Logger.debug('Draggable double pressed at %s' % (self.double_press))
            else:
                touch.grab(self)
                self.remove_widget(self.img)
                self.app.root.add_widget(self.img)
                #self.center = touch.pos
                self.img.center = touch.pos
            return True

        return super(DraggableImage, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):

        if touch.grab_current == self:
            self.img.center = touch.pos
        return super(DraggableImage, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            if self.grid.collide_point(*touch.pos):
                for cel in self.grid.cells:
                    if cel.collide_point(*touch.pos):
                        self.node.parent.clear_widgets()
                        self.app.root.remove_widget(self.img)
                        self.cell=cel
                        self.node.cell=cel
                        self.cell.add_widget(self.node)
                        self.add_widget(self.img)
                        touch.ungrab(self)
                        return True
                self.app.root.remove_widget(self.img)
                self.cell=1
                self.add_widget(self.img)
                touch.ungrab(self)
                return True
            else:
                self.node.parent.clear_widgets()
                self.app.root.remove_widget(self.img)
                self.cell.add_widget(self.node)
                self.add_widget(self.img)
                touch.ungrab(self)
        return super(DraggableImage, self).on_touch_up(touch, *args)

class ConnectorForward(ToggleButton):
    
    grid=ObjectProperty(None)
    connections=ListProperty([])
    node=ObjectProperty(None)
    matching_connection=ObjectProperty(None)
    connector_color=ListProperty([1, 1, 1])
    
    def __init__(self, **kwargs):
        
        super(ConnectorForward, self).__init__(**kwargs)
        self.background_down='src/img/drag_node_down_small.png'
        self.background_normal='src/img/drag_node_small.png'
        self.group='front'
        self.bind(on_press=self.create_connections)
        
    def create_connections(self, *args):
        keep_going=False
        
        for node in self.grid.nodes:
            if node.receiver.state=='down':
                keep_going=True
                Logger.debug('FlowChart: Active Receiver Detected')
        
        if keep_going:
                
            for node in self.grid.nodes:
                if node.receiver.state=='down':
                    self.state='normal'
                    node.receiver.state='normal'
                    connector = Connector(line_color=self.connector_color)
                    self.connections.append(connector)
                    self.node.connections.append(node)
                    self.matching_connection=node
                    Logger.debug('FlowChart: Matching Connector appended')
                    
            #Add the connections to the widget
            for connect in self.connections:
                self.add_widget(connect)
                connect.front=self.center
                connect.back=self.matching_connection.receiver.center
                Logger.debug('FlowChart: Connections Updated')
    
class ConnectorBack(ToggleButton):
    app=ObjectProperty(None)
    def __init__(self, **kwargs):
        
        super(ConnectorBack, self).__init__(**kwargs)
        self.background_down='src/img/drag_node_down_small.png'
        self.background_normal='src/img/drag_node_small.png'
        self.group='back'
        self.bind(on_press=self.app.create_connections)

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
    
    row1=ObjectProperty(None)
    row2=ObjectProperty(None)
    row3=ObjectProperty(None)
    
    def __init__(self, **kwargs):
        
        super(FlowChartNode, self).__init__(**kwargs)
        
        con = ConnectorForward(grid=self.grid, node=self)
        Logger.debug('Flowchart: ConnectorNode: Connector Node initialized with grid %s' % (self.grid))
        rec = ConnectorBack(app=self.app)
        self.connector = con
        self.receiver = rec

        Clock.schedule_once(self.build_widget)
        
    def build_widget(self, *args):
        row1 = BoxLayout(size_hint=[1, 0.3])
        row2 = BoxLayout(size_hint=[1, 0.4])
        row3 = BoxLayout(size_hint=[1, 0.3])
        self.row1=row1
        self.row2=row2
        self.row3=row3
        buf1 = BoxLayout(size_hint=[0.25, 1])
        buf2 = BoxLayout(size_hint=[0.25, 1])
        buf3 = BoxLayout(size_hint=[0.25, 1])
        buf4 = BoxLayout(size_hint=[0.25, 1])
        
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
        
    def clear_all_widgets(self, *args):
        self.clear_widgets()
        self.connector.clear_widgets()