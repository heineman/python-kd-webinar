"""
    KD Tree Implementation for 8/19/2015 Webinar
    Iteration: 0
    
    Author: George Heineman
"""

from region import maxRegion, X, Y

HORIZONTAL = 0
VERTICAL   = 1

class KDNode:

    def __init__(self, pt, orient, region = maxRegion):
        """Create empty KDNode."""
        self.point  = pt
        self.orient = orient
        self.above  = None
        self.below  = None
        self.region = region

    def createChild(self, pt, below):
        """Create child node (either above or below) given node with pt."""
        r = self.region.copy()
        if self.orient == VERTICAL:
            if below:
                r.x_max = self.point[X]
            else:
                r.x_min = self.point[X]
        else:
            if below:
                r.y_max = self.point[Y]
            else:
                r.y_min = self.point[Y]

        return KDNode(pt, 1-self.orient, r)

    def isBelow(self, pt):
        """Is point below current node."""
        if self.orient == VERTICAL:
            return pt[X] < self.point[X]
        return pt[Y] < self.point[Y]

    def add(self, pt):
        """
        Add point to the KD Tree rooted at this node.
        Return True if updated structure.
        """
        if self.point == pt:
            return False

        if self.isBelow(pt):
            if self.below:
                return self.below.add(pt)
            else:
                self.below = self.createChild(pt, True)
        else:
            if self.above:
                return self.above.add(pt)
            else:
                self.above = self.createChild(pt, False)

        return True
    
class KDTree:

    def __init__(self):
        """Create empty KD Tree."""
        self.root = None

    def add(self, pt):
        """Add Point to KD Tree."""

        if self.root:
            return self.root.add(pt)
        else:
            self.root = KDNode(pt, VERTICAL)
            return True

    def contains(self, pt):
        """Determines whether KD Tree has given point."""
        n = self.root
        while n:
            if n.point == pt:
                return True

            if n.isBelow(pt):
                n = n.below
            else:
                n = n.above
    
        return False
