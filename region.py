"""
    Defined rectangular region for use in KD-tree.

    Author: George Heineman
"""

maxValue = 2147483647
minValue = -2147483648

# Helps for more readable code
X = 0
Y = 1

class Region:
    """Represents region in Cartesian space."""

    def __init__(self, xmin,ymin, xmax,ymax):   
        """
        Creates region from two points (xmin,ymin) to (xmax,ymax).
        If these are not the bottom left and top right coordinates
        for a region, this constructor will properly compute them.
        """
        self.x_min = xmin if xmin < xmax else xmax
        self.y_min = ymin if ymin < ymax else ymax
        self.x_max = xmax if xmax > xmin else xmin
        self.y_max = ymax if ymax > ymin else ymin

    def copy(self):
        """Return copy of region."""
        return Region(self.x_min, self.y_min, self.x_max, self.y_max)

    def unionPoint(self, pt):
        """Return new region as union of region and point."""
        mx1 = min(self.x_min, pt[X])
        mx2 = max(self.x_max, pt[X])
        my1 = min(self.y_min, pt[Y])
        my2 = max(self.y_max, pt[Y])
        
        return Region(mx1, my1, mx2, my2)

    def containsPoint(self, point):
        """Returns True if point contained in rectangle."""
        if point[X] < self.x_min: return False
        if point[X] > self.x_max: return False
        if point[Y] < self.y_min: return False
        if point[Y] > self.y_max: return False
        
        return True
         
    def containsRegion(self, region):
        """Returns True if region contained in rectangle."""
        if region.x_min < self.x_min: return False
        if region.x_max > self.x_max: return False
        if region.y_min < self.y_min: return False
        if region.y_max > self.y_max: return False
        
        return True
    
    def __repr__(self):
        """Return string representation."""
        return "({},{} , {},{})".format(self.x_min, self.y_min,
                                        self.x_max, self.y_max)

# default maximum region
maxRegion = Region(minValue, minValue, maxValue, maxValue)
