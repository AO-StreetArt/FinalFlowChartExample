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
from kivy.logger import Logger

#This class defines a draggable object which will be
#added to the layout it's dropped on.  This allows for
#a sortable list that can be dragged into the flow node_editor
#The is_draggable property is exposed to allow for a button-like 
#functionality when it is off, and a dragable functionality when
#it is on.  This means we can have a connection mode to create
#connections between the nodes
class DraggableOption(Magnet):
    
    #The Label being added
    img = ObjectProperty(None, allownone=True)
    
    #The app being added to
    app = ObjectProperty(None)
    
    #The grid layout of the workflow list
    grid_layout = ObjectProperty(None)
    
    #The float layout of the workflow list
    float_layout = ObjectProperty(None)
    
    #The node editor (Drag Grid) on the page being dragged to
    grid = ObjectProperty(None)

    def on_img(self, *args):
        self.clear_widgets()

        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        
        #If the touch hits the widget
        if self.collide_point(*touch.pos):
            
            #Grab the widget and remove the image from it
            touch.grab(self)
            self.remove_widget(self.img)
            self.app.root.add_widget(self.img)
            self.img.center = touch.pos
            return True

        return super(DraggableOption, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):

        #If the widget is grabbed
        if touch.grab_current == self:
            #Move the image to the touch position
            self.img.center = touch.pos
            
            #If the touch hits the grid layout
            if self.grid_layout.collide_point(*touch.pos):
                #Remove the widget from it's layout
                self.grid_layout.remove_widget(self)
                self.float_layout.remove_widget(self)

                #Loop through the children of the grid layout and determine if 
                #the touch collides with them
                for i, c in enumerate(self.grid_layout.children):
                    if c.collide_point(*touch.pos):
                        self.grid_layout.add_widget(self, i+1)
                        break
                else:
                    self.grid_layout.add_widget(self)
                    
            #Else If the touch hits the box layout
            elif self.float_layout.collide_point(*touch.pos):
                #If the parent of the widget is currently the grid layout
                if self.parent == self.grid_layout:
                    #Remove it from the grid layout and add it to the float layout
                    self.grid_layout.remove_widget(self)
                    self.float_layout.add_widget(self)
                    
            #Else put the widget back in the grid layout
            else:
                if self.parent == self.float_layout:
                    self.float_layout.remove_widget(self)
                    self.grid_layout.add_widget(self)

        return super(DraggableOption, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        add_image=True
        self.app.root.remove_widget(self.img)
        #If the widget is grabbed
        if touch.grab_current == self:
            #If the touch collides with the drag grid
            if self.grid.collide_point(*touch.pos):
                #Loop through the cells in the drag grid and determine if 
                #the touch collides with them
                for cell in self.grid.cells:
                    if cell.collide_point(*touch.pos):
                        
                        #Add a flowchart node to the app with the specified label/image and cell
                        self.app.add_flowchart_node(cell, self.img)
                        
                        #Remove this widget from the list
                        if self.parent == self.grid_layout:
                            self.grid_layout.remove_widget(self)
                        elif self.parent == self.float_layout:
                            self.float_layout.remove_widget(self)
                        add_image=False
                        
            if add_image:
                self.add_widget(self.img)
            touch.ungrab(self)
            return True

        return super(DraggableOption, self).on_touch_up(touch, *args)