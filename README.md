#Flowcharting Example
This repository is currently under active development.

This is designed to be a framework upon which Kivy Flowcharting applications can be built.

Built using the Garden Magnet.  The compatible version is included in the src folder, but you can find the source for that [here](https://github.com/kivy-garden/garden.magnet).

##DragGrid Class
The DragGrid Class defines a Grid Layout with a pre-defined number of rows and columns.  Each Cell in the DragGrid is really a Box Layout with a few extra properties.  This gives a couple of advantages:

- Easy to Animate
The DragGrid is very easy to animate and create the 'snap to grid' functionality.  Effectively, each Cell can be used as a target for catching callbacks.

- Easy to Reference Cells
The Grid offers some convinience methods to return cells from it.  Currently, this includes:
  - get_cell(row, column)
  - clear_cells()
  - get_next_cell(origin_row, origin_column)

- Simple to Add/Remove Widgets
The grid lets us use lines like:
```python
button = Button(text='Button')
root.grid.get_cell(0, 0).add_widget(my_button)

root.grid.get_cell(0, 0).clear_widgets()
```

##Draggables
We have a draggable to move from the draggable list to the flowchart editor, another to be the label in the flowchart editor, and one last to be the connector in the flowchart editor.  These are still under construction.

##FlowChartNode Class
This combines a button, a draggable label, and a connector node into a flow chart node, that can be customized and used in different ways.  At it's heart, it will support drag-n-drop as well as the ability to connect multiple nodes together.
