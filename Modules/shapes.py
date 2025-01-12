#define shapes for matching game

class Shapes():
    """Define shapes."""

    def __init__(self, mg):
        """Initiate shape attributes."""
        self.donut = 'donut'
        self.square = 'square'
        self.diamond = 'diamond'
        self.lines = 'lines'
        self.oval = 'oval'

        self.all_shapes = (self.donut, self.square, self.diamond, self.lines, self.oval)
        