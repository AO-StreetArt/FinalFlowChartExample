# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 19:05:49 2015

@author: alex
"""

from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty

#This class defines the line drawn between two nodes
class Connector(Widget):
    
    #Front and Back vertices, the line is drawn in between
    #2 Entry Lists
    front = ListProperty([0, 0])
    back = ListProperty([1, 1])
    
    #The color of the lines
    #3 Entry Lists
    line_color = ListProperty([1, 1, 1])
    
    ellipse_diameter = NumericProperty(20)
    
    def __init__(self, **kwargs):
        super(MenuConnector, self).__init__(**kwargs)
        self.bind(front=self.set_front, back=self.set_back, line_color=self.set_color)
    
    def set_front(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(self.line_color[0], self.line_color[1], self.line_color[2])
            Line(points=[self.front[0], self.front[1], self.back[0], self.back[1]])
    
    def set_back(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(self.line_color[0], self.line_color[1], self.line_color[2])
            Line(points=[self.front[0], self.front[1], self.back[0], self.back[1]])
    
    def set_color(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(self.line_color[0], self.line_color[1], self.line_color[2])
            Line(points=[self.front[0], self.front[1], self.back[0], self.back[1]])