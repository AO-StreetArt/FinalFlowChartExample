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
my_button = Button(text='Button')
root.grid.get_cell(0, 0).add_widget(my_button)

root.grid.get_cell(0, 0).clear_widgets()
```

It is recommended that you add an ObjectProperty to your root widget with a name like 'drag_grid'.  Then, you can add the draggable grid into your .kv files and use it with standard kivy designs.

##Draggables
The Flow Chart Node is a created using a 7 line series:

```python
lbl = Label(text='Test')
drag_label = DraggableImage(img=lbl, app=self, grid=root.drag_grid, cell=root.drag_grid.cells[0])
drag = FlowChartNode(app=self, grid=root.drag_grid, cell=root.drag_grid.cells[0], label=drag_label)
drag_label.node = drag
root.drag_grid.cells[0].add_widget(drag)
root.drag_grid.cells[0].nodes.append(drag)
root.drag_grid.nodes.append(drag)
```

From there, it functions pretty much independently.  Users can drag and drop it around the grid, or use the toggle buttons to create connections.

You can access a list of nodes on the grid at root.drag_grid.nodes, which is a ListProperty.

###Options
the label property of the flowchartnode is designed to allow for any type of widget to be utilized.  The Draggable Image can be replaced with a more static image or it can be used and any widget class can be inserted into it using the lbl property.

Several other properties are necessary to pass in on construction.  This is to allow for the code to interact.  Don't forget them!

You also need to append the node into root.drag_grid.cells[i].nodes ListProperty and the root.drag_grid.nodes ListProperty

##Connector
The connector is a simple widget.  It doesn't rely on pos and size, like other widgets, but instead has exactly two ListProperty objects: front and back.  These are 2 number vertices for the position of the front and back of the line.  This makes drawing connections between two nodes simple and quick.

##Making new Draggables
The draggable is the most difficult piece of the code.  Take care when writing your own to hit all the necessary properties, as things are tracked at several levels.
