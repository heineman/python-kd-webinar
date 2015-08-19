"""
    Sample generator
"""

def onlyEven(values):
    """Select only even values as iterator."""
    for v in values:
        if v % 2 == 0:
            yield v

