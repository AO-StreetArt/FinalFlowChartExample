# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 16:27:01 2015

A Draggable Image for use in the Workflow List
Can be dropped into the node editor

@author: abarry
"""
from Magnet import Magnet
from kivy.properties import ObjectProperty
from kivy.clock import Clock

#This class defines a draggable object which will be
#added to the layout it's dropped on.  This allows for
#a sortable list that can be dragged into the flow node_editor
#The is_draggable property is exposed to allow for a button-like 
#functionality when it is off, and a dragable functionality when
#it is on.  This means we can have a connection mode to create
#connections between the nodes
class DraggableImage(Magnet):
    
    #The Label being added
    img = ObjectProperty(None, allownone=True)
    
    #The app being added to
    app = ObjectProperty(None)
    
    #The grid layout of the workflow list
    grid_layout = ObjectProperty(None)
    
    #The float layout of the workflow list
    float_layout = ObjectProperty(None)
    
    #The node editor (Drag Grid) on the page being dragged to
    node_editor = ObjectProperty(None)

    def on_img(self, *args):
        self.clear_widgets()

        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        if self.down:
            self.down = False
        else:
            self.down = True
        if self.collide_point(*touch.pos):
            if self.is_draggable:
                touch.grab(self)
                self.remove_widget(self.img)
                self.app.root.add_widget(self.img)
                self.center = touch.pos
                self.img.center = touch.pos
            else:
                if self.press:
                    self.press = False
                else:
                    self.press = True
            return True

        return super(DraggableImage, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):

        if touch.grab_current == self:
            self.img.center = touch.pos
            if self.grid_layout.collide_point(*touch.pos):
                self.grid_layout.remove_widget(self)
                self.float_layout.remove_widget(self)

                for i, c in enumerate(self.grid_layout.children):
                    #We need to keep things in the floatlayout longer
                    if c.collide_point(*touch.pos):
                        self.grid_layout.add_widget(self, i+1)
                        break
                else:
                    self.grid_layout.add_widget(self)
            elif self.box_layout.collide_point(*touch.pos):
                if self.parent == self.grid_layout:
                    self.grid_layout.remove_widget(self)
                    self.float_layout.add_widget(self)
            else:
                if self.parent == self.grid_layout:
                    self.grid_layout.remove_widget(self)
                if self.parent == self.float_layout:
                    self.float_layout.remove_widget(self)
                self.grid_layout.add_widget(self)

                self.center = touch.pos
        return super(DraggableImage, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            self.app.root.add_widget(self.img)
            if self.node_editor.collide_point(*touch.pos):
                for cell in self.node_editor.cells:
                    if cell.collide_point(*touch.pos):
                        #TO-DO: This needs to trigger an event in the root widget which we can bind to
                        if self.parent == self.grid_layout:
                            self.grid_layout.remove_widget(self)
                        elif self.parent == self.float_layout:
                            self.float_layout.remove_widget(self)
            touch.ungrab(self)
            return True

        return super(DraggableImage, self).on_touch_up(touch, *args)