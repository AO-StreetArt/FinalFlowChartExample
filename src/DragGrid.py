# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 15:41:35 2015

@author: abarry
"""

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, ReferenceListProperty
from kivy.logger import Logger

#A Cell in the DragGrid
class DragGridCell(BoxLayout):
    
    #Object Property to store the Grid it's attached to
    grid=ObjectProperty(None)
    
    #The row number of the cell
    row=NumericProperty(None)
    
    #The column number of the cell
    col=NumericProperty(None)
    
    #The position of the cell (row, column)
    pos=ReferenceListProperty(row, col)
    
    #List of flow chart nodes currently occupying this cell
    nodes=ListProperty([])
        
    #Is the cell empty
    def is_empty(self):
        if len(self.nodes) == 0:
            return True
        else:
            return False

#The Dragging Grid
class DragGrid(GridLayout):
    
    #A list of the cells in the drag grid
    cells=ListProperty([])
    
    #A list of nodes currently occuppying the drag grid
    nodes=ListProperty([])
    
    #The size (length and width) of the drag grid
    size=NumericProperty(3)
    
    #A list of connections
    #The first row is the front node, the next row is the back node
    connections=ListProperty([])
    
    #Called when initialized to add the cells to the grid
    def __init__(self, **kwargs):

        super(DragGrid, self).__init__(**kwargs)
        self.cols=self.size
        for i in range(0, self.size):
            for j in range(0, self.size):
                cell=DragGridCell(grid=self, row=i, col=j, orientation='vertical')
                self.cells.append(cell)
                self.add_widget(cell)
                
        self.connections.append([])
        self.connections.append([])
        Logger.debug('Flowchart: DragGrid: Drag Grid Filled')
    
    #Return the cell with the given row (x) and column (y)
    def get_cell(self, x, y):
        for cell in self.cells:
            if cell.row == x and cell.col == y:
                return cell
        return 0
        
    #Clear all the widgets from every cell in the 
    def clear_cells(self):
        for cell in self.cells:
            cell.clear_widgets()
            
    #Get the next cell, based on the origin.
    #The method looks for the closest empty cell in the grid to the origin position
    def get_next_cell(self, origin_row, origin_col):
        ordered_cells=[]
        distances=[]
        positions=[]
        min_distance=99999
        min_pos=[(0,0)]
        for cell in self.cells:
            if cell.is_empty():
                ordered_cells.append(cell)
                for o_cell in ordered_cells:
                    distances.append((((o_cell.row - origin_row) ** 2) + ((o_cell.col - origin_col) ** 2)) ** 0.5)
                    positions.append(o_cell.pos)
        
        i=0
        for dist in distances:
            if dist < min_distance and dist != 0:
                min_distance = dist
                min_pos = positions[i]
            i+=1
            
        return self.get_cell(min_pos[0], min_pos[1])
        