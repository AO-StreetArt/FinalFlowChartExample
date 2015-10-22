# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 16:27:01 2015

A Draggable Label for use as a flow chart widget
A Connector and Receiver can be added/removed to it's node and move as it's moved around

@author: abarry
"""
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from Magnet import Magnet
from kivy.logger import Logger

class DraggableLabel(Magnet):
    
    #The label being added
    img = ObjectProperty(None, allownone=True)
    
    #The app being added to
    app = ObjectProperty(None)
    
    #The Grid the widget is in
    grid = ObjectProperty(None)
    
    #The cell the widget is currently in
    cell = ObjectProperty(None)
    
    #The flowchart node that contains the draggable label
    #It will also contain a connector and reciever
    node = ObjectProperty(None)

    def on_img(self, *args):
        self.clear_widgets()
        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        touch.grab(self)
        self.clear_widgets()
        self.app.root.add_widget(self.img)
        self.center = touch.pos
        self.img.center = touch.pos
        return True

        return super(DraggableLabel, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):

        if touch.grab_current == self:
            self.img.center = touch.pos
        return super(DraggableLabel, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            if self.grid.collide_point(*touch.pos):
                for cel in self.grid.cells:
                    if cel.collide_point(*touch.pos):
                        self.node.parent.clear_widgets()
                        self.cell.nodes.remove(self.node)
                        self.app.root.remove_widget(self.img)
                        self.cell=cel
                        self.cell.add_widget(self.node)
                        self.cell.nodes.append(self.node)
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
        return super(DraggableLabel, self).on_touch_up(touch, *args)