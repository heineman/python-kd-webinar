"""
    Demonstration application for range search using kd tree.
    Left mouse adds point, right mouse click begins drag of rectangle.

    Iteration: 2
    Author: George Heineman
"""

import tkinter
from kd2 import KDTree, X, Y, VERTICAL
from region import Region, minValue, maxValue

BoxSize = 4    # size of box representing point
Size = 400     # size of canvas containing drawn KD-Tree


class KDTreeApp:

    def __init__(self):
        """App for creating KD tree dynamically and executing range queries."""
        
        self.tree = KDTree()
        
        # for range query
        self.selectedRegion = None
        self.queryRect = None
       
        master = tkinter.Tk()
        master.maxsize(width=Size, height=Size+26)
        master.minsize(width=Size, height=Size+26)
        master.title('KD Tree Drawing and Query Application')
        self.w = tkinter.Frame(master, width=Size, height=Size+26)
        self.canvas = tkinter.Canvas(self.w, width=Size, height=Size)        
        self.paint()   

        b = tkinter.Button(master, text="Reset", command=self.reset)
        b.pack()

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-3>", self.range)   # when right mouse clicked
        self.canvas.bind("<ButtonRelease-3>", self.clear)
        self.canvas.bind("<B3-Motion>", self.range)  # only when right mouse dragged

        # Different bindings on Macintosh platform
        self.canvas.bind("<Button-2>", self.range)   # when right mouse clicked
        self.canvas.bind("<ButtonRelease-2>", self.clear)
        self.canvas.bind("<B2-Motion>", self.range)  # only when right mouse dragged

        self.canvas.pack()
        self.w.pack()

    def reset(self):
        """Reset to initial state."""
        self.tree = KDTree()
        self.paint()

    def toCartesian(self, y):
        """Convert tkinter point into Cartesian."""
        return Size - y

    def toTk(self,y):
        """Convert Cartesian into tkinter point."""
        if y == maxValue: return 0
        tk_y = Size
        if y != minValue:
            tk_y -= y
        return tk_y
         
    def clear(self, event):
        """End of range search."""
        self.selectedRegion = None
        self.paint()
        
    def range(self, event):
        """Initiate a range search using a selected rectangular region."""
        
        p = (event.x, self.toCartesian(event.y))
         
        if self.selectedRegion is None:
            self.selectedStart = Region(p[X],p[Y],  p[X],p[Y])
        self.selectedRegion = self.selectedStart.unionPoint(p)
        
        self.paint()
        
        # return (node,sub-tree) where sub-tree is True if draining entire tree
        # rooted at node. Draw these as shaded red rectangle to identify whole
        # sub-tree is selected.
        for pair in self.tree.range(self.selectedRegion):
            p = pair[0].point
            
            if pair[1]:
                self.canvas.create_rectangle(pair[0].region.x_min, self.toTk(pair[0].region.y_min), 
                                             pair[0].region.x_max, self.toTk(pair[0].region.y_max),
                                             fill='Red', stipple='gray12')
            else:
                self.canvas.create_rectangle(p[X] - BoxSize, self.toTk(p[Y]) - BoxSize, 
                                             p[X] + BoxSize, self.toTk(p[Y]) + BoxSize, fill='Red')

        self.queryRect = self.canvas.create_rectangle(self.selectedRegion.x_min, self.toTk(self.selectedRegion.y_min),  
                                                     self.selectedRegion.x_max, self.toTk(self.selectedRegion.y_max), 
                                                     outline='Red', dash=(2, 4))
        
    def click(self, event):
        """Add point to KDtree."""
        p = (event.x, self.toCartesian(event.y))
        self.tree.add(p)
        self.paint()

    def drawPartition (self, r, p, orient):
        """Draw partitioning line and points itself as a small square."""
        if orient == VERTICAL:
            self.canvas.create_line(p[X], self.toTk(r.y_min), p[X], self.toTk(r.y_max))
        else:
            xlow = r.x_min
            if r.x_min <= minValue: xlow = 0
            xhigh = r.x_max
            if r.x_max >= maxValue: xhigh = Size

            self.canvas.create_line(xlow, self.toTk(p[Y]), xhigh, self.toTk(p[Y]))

        self.canvas.create_rectangle(p[X] - BoxSize, self.toTk(p[Y]) - BoxSize,
                                     p[X] + BoxSize, self.toTk(p[Y]) + BoxSize,
                                     fill='Black')

    def visit (self, n):
        """ Visit node to paint properly."""
        if n == None: return

        self.drawPartition(n.region, n.point, n.orient)
        self.visit (n.below)
        self.visit (n.above)

    def paint(self):
        """Paint KD Tree by visiting all nodes."""
        self.canvas.delete(tkinter.ALL)
        self.visit(self.tree.root)
    
if __name__ == "__main__":
    app = KDTreeApp()
    app.w.mainloop()
