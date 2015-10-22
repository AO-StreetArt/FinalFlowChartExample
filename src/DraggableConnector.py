# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:52:47 2015

@author: alex
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 16:27:01 2015

A Draggable Connector
When dragged onto a cell with a node, it removes the connector end note
and snaps a connector between the nodes (at global level)

@author: abarry
"""
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty
from Magnet import Magnet
from kivy.uix.button import Button
from kivy.logger import Logger

class SimpleConnectorButton(Button):
    #The Grid being worked on
    grid=ObjectProperty(None)
    
    #The Cell the button currently resides in
    cell=ObjectProperty(None)
    
    #The connector node the button belongs to
    node=ObjectProperty(None)

class DraggableConnector(Magnet):
    
    #The label being added
    img = ObjectProperty(None, allownone=True)
    
    #The app being added to
    app = ObjectProperty(None)
    
    #The Grid the widget is in
    grid = ObjectProperty(None)
    
    #The cell the widget is currently in
    cell = ObjectProperty(None)
    
    #The flowchart node that contains the draggable connector
    #It will also contain a label and reciever
    node = ObjectProperty(None)
    
    #0 if the current cell is empty (no full nodes)
    #1 if the current cell is not
    is_match = NumericProperty(0)

    def on_img(self, *args):
        self.clear_widgets()
        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        touch.grab(self)
        self.remove_widget(self.img)
        self.app.root.add_widget(self.img)
        self.center = touch.pos
        self.img.center = touch.pos
        return True

        return super(DraggableConnector, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):

        if touch.grab_current == self:
            self.img.center = touch.pos
        return super(DraggableConnector, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            #Clear the node widgets
            self.node.clear_all_widgets()
            #Add the node back with no connector
            self.node.build_widget_no_connector()
            Logger.debug('Widget removed from node (%s, %s)' % (self.cell.row, self.cell.col))
            if self.grid.collide_point(*touch.pos):
                for cel in self.grid.cells:
                    if cel.collide_point(*touch.pos):
                        if cel.is_empty():
                            self.app.root.remove_widget(self.img)
                            self.parent.clear_widgets()
                            self.cell=cel
                            Logger.debug('Widget cell updated to (%s, %s)' % (self.cell.row, self.cell.col))
                            self.node.add_widget(self)
                            self.add_widget(self.img)
                            touch.ungrab(self)
                            return True
                        else:
                            self.is_match
                            self.app.update_connectors(self.node, self)
                            
                self.app.root.remove_widget(self.img)
                self.add_widget(self.img)
                touch.ungrab(self)
                return True
#            else:
#                self.app.root.remove_widget(self.img)
#                self.node.add_widget(self)
#                self.node.add_widget(self.node.buf)
#                self.add_widget(self.img)
#                touch.ungrab(self)
        return super(DraggableConnector, self).on_touch_up(touch, *args)