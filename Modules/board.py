#board functions
from settings import Settings

class Board():
    """Represents the board."""

    def __init__(self):
        """Initiate attributes."""

        self.settings = Settings(self)
        self.define_board_margins()

    def define_board_margins(self):
        """Define x and y margin."""

        self.x_margin = int((self.settings.window_width - (self.settings.board_width
                             * (self.settings.box_size + self.settings.gap_size))) / 2)
        self.y_margin = int((self.settings.window_height - (self.settings.board_height
                             * (self.settings.box_size + self.settings.gap_size))) / 2)
